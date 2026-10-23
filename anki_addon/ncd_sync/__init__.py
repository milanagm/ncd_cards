"""NeetCode Insights Sync: pulls the latest cards from GitHub into Anki and syncs them to your other devices.

Runs after every AnkiWeb sync (so right after Anki's startup sync), every few hours while Anki is
open, and from Tools → "NeetCode Insights aktualisieren". The collection logic lives in core.py.
"""
import json
import os
import ssl
import tempfile
import time
import urllib.error
import urllib.request

from aqt import gui_hooks, mw
from aqt.operations import CollectionOp, QueryOp
from aqt.qt import QAction, qconnect
from aqt.utils import tooltip

from . import core

_running = False
_closing = False
_last_run = 0.0
_timer = None


def _config():
    return mw.addonManager.getConfig(__name__) or {}


def _download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "ncd-sync-anki-addon"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except urllib.error.URLError as e:
        if not isinstance(e.reason, ssl.SSLCertVerificationError):
            raise
    # Anki's bundled Python cannot always see the system certificates (macOS); certifi ships with Anki.
    import certifi

    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, timeout=30, context=context) as response:
        return response.read()


def run(manual=False):
    """Fetch cards.json and apply it. Automatic runs are throttled; manual runs always report back."""
    global _running, _last_run
    if _running or _closing or mw.col is None:
        return
    config = _config()
    if not manual and time.time() - _last_run < config.get("min_minutes_between_runs", 30) * 60:
        return
    _running, _last_run = True, time.time()
    QueryOp(
        parent=mw,
        op=lambda col: json.loads(_download(config["cards_url"]).decode("utf-8")),
        success=lambda payload: _apply(payload, config, manual),
    ).failure(lambda e: _finish(manual, error=e)).without_collection().run_in_background()


def _apply(payload, config, manual, imported=None):
    if _closing or mw.col is None:
        return _finish(manual)

    def succeeded(result):
        result.summary.imported = imported or 0
        _finish(manual, summary=result.summary, config=config)

    def failed(e):
        if isinstance(e, core.NeedsBootstrap) and imported is None:
            _bootstrap(payload, config, manual)
        else:
            _finish(manual, error=e)

    CollectionOp(
        parent=mw, op=lambda col: core.apply(col, payload, config.get("reschedule_recurring", True))
    ).success(succeeded).failure(failed).run_in_background()


def _bootstrap(payload, config, manual):
    """First run without the note type: import the deck package once, then apply cards.json."""
    def download(col):
        fd, path = tempfile.mkstemp(suffix=".apkg")
        with os.fdopen(fd, "wb") as f:
            f.write(_download(config["deck_url"]))
        return path

    def import_package(path):
        def done(result):
            os.unlink(path)
            _apply(payload, config, manual, imported=len(result.log.new))

        CollectionOp(parent=mw, op=lambda col: core.bootstrap(col, path)).success(done).failure(
            lambda e: _finish(manual, error=e)).run_in_background()

    QueryOp(parent=mw, op=download, success=import_package).failure(
        lambda e: _finish(manual, error=e)).without_collection().run_in_background()


def _finish(manual, summary=None, config=None, error=None):
    global _running
    _running = False
    if error is not None:
        tooltip(f"NeetCode Insights: Aktualisierung fehlgeschlagen ({error})", period=8000)
        return
    if summary is None:
        return
    if summary.changed or manual:
        tooltip(summary.message(), period=6000)
    if summary.changed and config.get("sync_after_update", True) and mw.pm.sync_auth() \
            and not mw.media_syncer.is_syncing():
        sync = getattr(mw, "on_sync_button_clicked", None) or mw.onSync
        sync()  # the sync_did_finish that follows is throttled by _last_run


def _on_profile_did_open():
    global _closing, _timer
    _closing = False
    can_auto_sync = getattr(mw, "can_auto_sync", lambda: False)
    if not can_auto_sync():  # no startup sync, so sync_did_finish will not trigger the first run
        mw.progress.single_shot(5000, run)
    hours = _config().get("interval_hours", 6)
    _timer = mw.progress.timer(int(hours * 3600 * 1000), run, True, parent=mw)


def _on_profile_will_close():
    global _closing, _timer
    _closing = True
    if _timer is not None:
        _timer.stop()
        _timer = None


gui_hooks.sync_did_finish.append(run)
gui_hooks.profile_did_open.append(_on_profile_did_open)
gui_hooks.profile_will_close.append(_on_profile_will_close)

_action = QAction("NeetCode Insights aktualisieren", mw)
qconnect(_action.triggered, lambda: run(manual=True))
mw.form.menuTools.addAction(_action)
