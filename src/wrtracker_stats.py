# -*- coding: utf-8 -*-

from helpers import dependency
from skeletons.gui.shared import IItemsCache


class AccountStats(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def update(self):
        dossier = self.itemsCache.items.getAccountDossier()
        if dossier is None:
            return None
        total = dossier.getTotalStats()
        return int(total.getWinsCount() or 0), int(total.getBattlesCount() or 0)
