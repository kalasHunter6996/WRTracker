# -*- coding: utf-8 -*-

import BigWorld

from frameworks.wulf import WindowLayer
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework import g_entitiesFactories, ScopeTemplates, ViewSettings
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import events, EVENT_BUS_SCOPE, g_eventBus
from gui.shared.personality import ServicesLocator

from wrtracker_stats import AccountStats


WR_TRACKER_VIEW = 'KALAS_WR_TRACKER_VIEW'
SWF_NAME = 'kalas.wrtracker.WrTrackerView.swf'


def win_rate(wins, battles):
    if battles <= 0:
        return 0.0
    return round(float(wins) * 100.0 / float(battles), 2)


def wins_to_target(wins, battles, target):
    if battles <= 0 or target >= 100.0:
        return 0
    if float(wins) * 100.0 / float(battles) >= target:
        return 0
    t = float(target) / 100.0
    n = int(max(0.0, (t * battles - wins) / (1.0 - t)))
    while float(wins + n) * 100.0 / float(battles + n) < target:
        n += 1
    return n


class WRTrackerView(View):
    def __init__(self, *args, **kwargs):
        super(WRTrackerView, self).__init__(*args, **kwargs)
        self._stats = AccountStats()

    def _populate(self):
        super(WRTrackerView, self)._populate()
        self._update()

    def _dispose(self):
        self._stats = None
        super(WRTrackerView, self)._dispose()

    def _update(self):
        if not self._stats.update():
            self.as_setData('', '', '', '')
            return
        wins = self._stats.wins
        battles = self._stats.battles
        wr = win_rate(wins, battles)
        half = (int(wr * 2.0) + 1) / 2.0
        whole = int(wr) + 1
        self.as_setData(
            '%.2f' % wr,
            '%.1f' % half,
            '%d' % wins_to_target(wins, battles, half),
            '%.1f|%d|%d' % (whole, wins_to_target(wins, battles, whole), battles)
        )

    def as_setData(self, wr, half, half_wins, whole_data):
        if self.flashObject is not None:
            self.flashObject.as_setData(wr, half, half_wins, whole_data)


def _on_app_initialized(event):
    if event.ns != APP_NAME_SPACE.SF_LOBBY:
        return
    app = ServicesLocator.appLoader.getApp(event.ns)
    if app is not None:
        try:
            app.loadView(SFViewLoadParams(WR_TRACKER_VIEW))
        except Exception as exc:
            print('[WRTracker] loadView failed: %s' % exc)


def setup():
    settings = ViewSettings(
        WR_TRACKER_VIEW,
        WRTrackerView,
        SWF_NAME,
        WindowLayer.TOP_WINDOW,
        None,
        ScopeTemplates.VIEW_SCOPE
    )
    g_entitiesFactories.addSettings(settings)
    g_eventBus.addListener(
        events.AppLifeCycleEvent.INITIALIZED,
        _on_app_initialized,
        EVENT_BUS_SCOPE.GLOBAL
    )


setup()
print('[WRTracker] prototype initialized')
