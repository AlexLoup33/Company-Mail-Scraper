__author__ = "AlexLoup33 | github.com/AlexLoup33"

import requests

from pathlib import Path
from bs4 import BeautifulSoup
from typing import NamedTuple
from openpyxl import Workbook
from openpyxl.worksheet._read_only import ReadOnlyWorksheet 
from openpyxl.chartsheet.chartsheet import Chartsheet
from tkinter import messagebox
from network import *

class EmailScrap(NamedTuple):
    email: str
    score: int

class InfoScrap(NamedTuple):
    company_name: str
    domain: str
    networkScrap: NetworkScrap | None
    emailPatern: str
    email : EmailScrap | None

class Queue:
    def __init__(self, size:int):
        self.queue = []
        self.size:int = size+1
        self.pointer:int = 0

    def enqueue(self, item):
        if self.is_full():
            return
        self.queue.append(item)
        self.pointer += 1

    def dequeue(self)->str:
        if self.is_empty():
            return ""
        self.pointer -= 1
        return self.queue.pop(0)
    
    def is_empty(self):
        return self.pointer <= 0
    
    def is_full(self):
        return self.pointer == self.size
    
    def display(self):
        for item in self.queue:
            print(item)

api_key = "d4d29913091c9954368733ea3f29bbced2a8c63e"

departementLinksSorted = {
    'Ain': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/ain-rdep/", 'Aisne': "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/aisne-rdep/", 
    'Allier':"https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/allier-rdep/", 'Alpes de Haute Provence' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/alpes-de-haute-provence-rdep/", 
    'Alpes Maritimes': "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/alpes-maritimes-rdep/", 'Ardèche': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/ardeche-rdep/", 
    'Ardennes' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/ardennes-rdep/", 'Aube': "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/aube-rdep/",
    'Aude': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/aude-rdep/", 'Aveyron' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/aveyron-rdep/", 
    'Bas Rhin' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/bas-rhin-rdep/", 'Bouches du Rhone' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/bouches-du-rhone-rdep/", 
    'Calvados': "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/calvados-rdep/", 'Cantal': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/cantal-rdep/",
    'Cote D Armor': "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/cote-d-armor-rdep/", "Cote D'or": "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/cote-d-or-rdep/",
    'Cher': "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/cher-rdep/", 'Charante' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/charente-rdep/",
    'Charante Maritime': "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/charente-maritime-rdep/", 'Correze' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/correze-rdep/",
    'Corse du Sud': "https://www.verif.com/top/revenue-r0/france-rcoun/corse-rreg/corse-du-sud-rdep/", 'Creuse': "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/creuse-rdep/",
    'Cote D Armor': "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/cote-d-armor-rdep/", 'Doubs': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/doubs-rdep/",
    'Drôme': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/drome-rdep/", 'Deux Sevres' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/deux-sevres-rdep/",
    'Eure': "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/eure-rdep/", 'Eure et Loir': "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/eure-et-loir-rdep/",
    'Essonne' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/essonne-rdep/", 'Finistère': "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/finistere-rdep/",
    'Gard': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/gard-rdep/", 'Gers' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/gers-rdep/",
    'Gironde' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/gironde-rdep/", 'Haute Loire': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/-rdep/haute-loire-rdep/",
    'Haute Corse': "https://www.verif.com/top/revenue-r0/france-rcoun/corse-rreg/haute-corse-rdep/", 'Haute Garonne': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/haute-garonne-rdep/",
    'Haute Marne' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/haute-marne-rdep/", 'Haute Saône': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/haute-saone-rdep/",
    'Haute Savoie': "https://verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/haute-savoie-rdep/", 'Haute Vienne': "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/haute-vienne-rdep/",
    'Hautes Alpes': "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/hautes-alpes-rdep/", 'Hautes Pyrenees' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/hautes-pyrenees-rdep/",
    'Haut Rhin' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/haut-rhin-rdep/", 'Hauts de Seine' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/hauts-de-seine-rdep/",
    'Herault': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/herault-rdep/", 'Ille et Vilaine': "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/ille-et-vilaine-rdep/",
    'Indre': "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/indre-rdep/", 'Indre et Loire': "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/indre-et-loire-rdep/",
    'Isère': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/isere-rdep/", 'Jura': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/jura-rdep/",
    'Landes': "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/landes-rdep/", 'Loire': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/loire-rdep/",
    'Loire Atlantique' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/loire-atlantique-rdep/", 'Loiret': "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/loiret-rdep/",
    'Loir et Cher': "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/loir-et-cher-rdep/", 'Lot': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/lot-rdep/",
    'Lot et Garonne' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/lot-et-garonne-rdep/", 'Lozere': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/lozere-rdep/",
    'Maine et Loire' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/maine-et-loire-rdep/", 'Manche': "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/manche-rdep/",
    'Marne': "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/marne-rdep/", 'Mayenne': "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/mayenne-rdep/",
    'Meurthe et Moselle' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/meurthe-et-moselle-rdep/", 'Meuse': "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/meuse-rdep/",
    'Morbihan': "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/morbihan-rdep/", 'Moselle' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/moselle-rdep/",
    'Nièvre': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/nievre-rdep/", 'Nord': "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/nord-rdep/",
    'Oise' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/oise-rdep/", 'Orne' : "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/orne-rdep/",
    'Pas de Calais': "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/pas-de-calais-rdep/", 'Puy-de-Dôme': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/puy-de-dome-rdep/",
    'Pyrenees Atlantiques': "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/pyrenees-atlantiques-rdep/", 'Pyrenees Orientales' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/pyrenees-orientales-rdep/",
    'Rhône': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/rhone-rdep/", 'Saône et Loire': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/saone-et-loire-rdep/",
    'Savoie': "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/savoie-rdep/", 'Sarthe' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/sarthe-rdep/",
    'Seine Maritime': "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/seine-maritime-rdep/", 'Seine Saint Denis': "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/seine-saint-denis-rdep/",
    'Seine et Marne' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/seine-et-marne-rdep/", 'Somme' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/somme-rdep/",
    'Tarn': "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/tarn-rdep/", 'Tarn et Garonne' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/tarn-et-garonne-rdep/",
    'Territoire de Belfort': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/territoire-de-belfort-rdep/", 'Val d Oise' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/val-d-oise-rdep/",
    'Val de Marne': "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/val-de-marne-rdep/", 'Var' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/var-rdep/",
    'Vaucluse': "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/vaucluse-rdep/", 'Vendee': "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/vendee-rdep/",
    'Vienne' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/vienne-rdep/", 'Vosges': "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/vosges-rdep/",
    'Yonne': "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/yonne-rdep/", 'Yvelines' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/yvelines-rdep/"
}

#DepartementLinks but sorted by the number of the departement with the format 'Departement - number' : "link"
departementLinks =  {
    'Ain - 01' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/ain-rdep/", 'Aisne - 02' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/aisne-rdep/",
    'Allier - 03' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/allier-rdep/", 'Alpes de Haute Provence - 04' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/alpes-de-haute-provence-rdep/",
    'Hautes-Alpes - 05' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/hautes-alpes-rdep/", 'Alpes Maritimes - 06' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/alpes-maritimes-rdep/",
    'Ardèche - 07' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/ardeche-rdep/", 'Ardennes - 08' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/ardennes-rdep/",
    'Ariège - 09' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/ariege-rdep/", 'Aube - 10' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/aube-rdep/",
    'Aude - 11' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/aude-rdep/", 'Aveyron - 12' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/aveyron-rdep/",
    'Bouches du Rhône - 13' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/bouches-du-rhone-rdep/", 'Calvados - 14' : "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/calvados-rdep/",
    'Cantal - 15' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/cantal-rdep/", 'Charente - 16' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/charente-rdep/",
    'Charente Maritime - 17' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/charente-maritime-rdep/", 'Cher - 18' : "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/cher-rdep/",
    'Corrèze - 19' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/correze-rdep/", 'Corse du Sud - 2A' : "https://www.verif.com/top/revenue-r0/france-rcoun/corse-rreg/corse-du-sud-rdep/",
    'Haute Corse - 2B' : "https://www.verif.com/top/revenue-r0/france-rcoun/corse-rreg/haute-corse-rdep/", 'Côte d Or - 21' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/cote-d-or-rdep/",
    'Côtes d Armor - 22' : "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/cote-d-armor-rdep/", 'Creuse - 23' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/creuse-rdep/",
    'Dordogne - 24' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/dordogne-rdep/", 'Doubs - 25' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/doubs-rdep/",
    'Drôme - 26' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/drome-rdep/", 'Eure - 27' : "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/eure-rdep/",
    'Eure et Loir - 28' : "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/eure-et-loir-rdep/", 'Finistère - 29' : "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/finistere-rdep/",
    'Gard - 30' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/gard-rdep/", 'Haute Garonne - 31' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/haute-garonne-rdep/",
    'Gers - 32' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/gers-rdep/", 'Gironde - 33' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/gironde-rdep/",
    'Hérault - 34' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/herault-rdep/", 'Ille et Vilaine - 35' : "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/ille-et-vilaine-rdep/",
    'Indre - 36' : "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/indre-rdep/", 'Indre et Loire - 37' : "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/indre-et-loire-rdep/",
    'Isère - 38' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/isere-rdep/", 'Jura - 39' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/jura-rdep/",
    'Landes - 40' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/landes-rdep/", 'Loir et Cher - 41' : "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/loir-et-cher-rdep/",
    'Loire - 42' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/loire-rdep/", 'Haute Loire - 43' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/haute-loire-rdep/",
    'Loire Atlantique - 44' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/loire-atlantique-rdep/", 'Loiret - 45' : "https://www.verif.com/top/revenue-r0/france-rcoun/centre-val-de-loire-rreg/loiret-rdep/",
    'Lot - 46' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/lot-rdep/", 'Lot et Garonne - 47' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/lot-et-garonne-rdep/",
    'Lozère - 48' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/lozere-rdep/", 'Maine et Loire - 49' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/maine-et-loire-rdep/",
    'Manche - 50' : "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/manche-rdep/", 'Marne - 51' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/marne-rdep/",
    'Haute Marne - 52' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/haute-marne-rdep/", 'Mayenne - 53' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/mayenne-rdep/",
    'Meurthe et Moselle - 54' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/meurthe-et-moselle-rdep/", 'Meuse - 55' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/meuse-rdep/",
    'Morbihan - 56' : "https://www.verif.com/top/revenue-r0/france-rcoun/bretagne-rreg/morbihan-rdep/", 'Moselle - 57' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/moselle-rdep/",
    'Nièvre - 58' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/nievre-rdep/", 'Nord - 59' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/nord-rdep/",
    'Oise - 60' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/oise-rdep/", 'Orne - 61' : "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/orne-rdep/",
    'Pas de Calais - 62' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/pas-de-calais-rdep/", 'Puy de Dôme - 63' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/puy-de-dome-rdep/",
    'Pyrénées Atlantiques - 64' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/pyrenees-atlantiques-rdep/", 'Hautes Pyrénées - 65' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/hautes-pyrenees-rdep/",
    'Pyrénées Orientales - 66' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/pyrenees-orientales-rdep/", 'Bas Rhin - 67' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/bas-rhin-rdep/",
    'Haut Rhin - 68' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/haut-rhin-rdep/", 'Rhône - 69' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/rhone-rdep/",
    'Haute Saône - 70' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/haute-saone-rdep/", 'Saône et Loire - 71' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/saone-et-loire-rdep/",
    'Sarthe - 72' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/sarthe-rdep/", 'Savoie - 73' : "https://www.verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/savoie-rdep/",
    'Haute Savoie - 74' : "https://verif.com/top/revenue-r0/france-rcoun/auvergne-rhone-alpes-rreg/haute-savoie-rdep/", 'Paris - 75' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/paris-rdep/",
    'Seine Maritime - 76' : "https://www.verif.com/top/revenue-r0/france-rcoun/normandie-rreg/seine-maritime-rdep/", 'Seine et Marne - 77' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/seine-et-marne-rdep/",
    'Yvelines - 78' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/yvelines-rdep/", 'Deux Sèvres - 79' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/deux-sevres-rdep/",
    'Somme - 80' : "https://www.verif.com/top/revenue-r0/france-rcoun/hauts-de-france-rreg/somme-rdep/", 'Tarn - 81' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/tarn-rdep/",
    'Tarn et Garonne - 82' : "https://www.verif.com/top/revenue-r0/france-rcoun/occitanie-rreg/tarn-et-garonne-rdep/", 'Var - 83' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/var-rdep/",
    'Vaucluse - 84' : "https://www.verif.com/top/revenue-r0/france-rcoun/provence-alpes-cote-d-azur-rreg/vaucluse-rdep/", 'Vendée - 85' : "https://www.verif.com/top/revenue-r0/france-rcoun/pays-de-la-loire-rreg/vendee-rdep/",
    'Vienne - 86' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/vienne-rdep/", 'Haute Vienne - 87' : "https://www.verif.com/top/revenue-r0/france-rcoun/nouvelle-aquitaine-rreg/haute-vienne-rdep/",
    'Vosges - 88' : "https://www.verif.com/top/revenue-r0/france-rcoun/grand-est-rreg/vosges-rdep/", 'Yonne - 89' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/yonne-rdep/",
    'Territoire de Belfort - 90' : "https://www.verif.com/top/revenue-r0/france-rcoun/bourgogne-franche-comte-rreg/territoire-de-belfort-rdep/", 'Essonne - 91' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/essonne-rdep/",
    'Hauts de Seine - 92' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/hauts-de-seine-rdep/", 'Seine Saint Denis - 93' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/seine-saint-denis-rdep/",
    'Val de Marne - 94' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/val-de-marne-rdep/", 'Val d Oise - 95' : "https://www.verif.com/top/revenue-r0/france-rcoun/ile-de-france-rreg/val-d-oise-rdep/",
    'Guadeloupe - 971' : "https://www.verif.com/top/revenue-r0/france-rcoun/dom-rreg/guadeloupe-rdep/", 'Martinique - 972' : "https://www.verif.com/top/revenue-r0/france-rcoun/dom-rreg/martinique-rdep/",
    'Guyane - 973' : "https://www.verif.com/top/revenue-r0/france-rcoun/dom-rreg/guyane-rdep/", 'La Réunion - 974' : "https://www.verif.com/top/revenue-r0/france-rcoun/dom-rreg/la-reunion-rdep/",
    'Mayotte - 976' : "https://www.verif.com/top/revenue-r0/france-rcoun/dom-rreg/mayotte-rdep/"
}


"""
Const who use Path lib to get the relative path of the directory 'save' and 'savetab' in the project for 
saving the csv file and the tabsheet file
"""
csvPath = Path(__file__).parent.joinpath("save")
tabPath = Path(__file__).parent.joinpath("savetab")

"""
Checking for the existence of the directories 'save' and 'savetab' and creating them if they don't exist
save is used to save the csv file generated by the program and who contain the basics informations of the companies (name, domain)
savetab is used to save the tabsheet file generated by the program and who contain all the 
informations findable of the companies and contain in the class InfoScrap (company name, domain, email, email score, contact page, 
facebook, twitter, linkedin)
Note: the tabsheet can not contain all the informations of the companies, because some companies don't have a contact page, or 
hide somes informations on their website
"""
if not csvPath.exists():
    csvPath.mkdir()
if not tabPath.exists():
    tabPath.mkdir()

def scrap(url:str, number:int, csvFileName:str, tabName:str, tabFileName:str)->None:
    print(f"Started to scrap at url {url}")
    """
    Get the html element of the page given, and parse it with BeautifulSoup (for the version, we will use only verif.com pages)
    At least, add the option to give other params like a list of company names, or a list of company domains.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    """
    Get the value in the span with class "MuiTypography-root MuiTypography-titleDesktopH4 css-1ltityp" who contain the number
    of companies in the region and compare with the number of companies the user wants.
    Also check if the element exist on the page by shuting down the function it if it's None because it's mean the page isn't
    a verif.com page or a good one to scrap
    """
    TotalCompaniesHtmlElement = soup.find_all('span', class_="MuiTypography-root MuiTypography-titleDesktopH4 css-1ltityp")
    assert TotalCompaniesHtmlElement is not None


    TotalCompanies:int = int(extractFloatFromString(TotalCompaniesHtmlElement[0].text.strip()))
    size:int = (TotalCompanies if number > TotalCompanies else number)

    """
    Initialize the queue with the size of the number of companies desired
    Note: The queue will not necessary be full, if the verif page of the company doesn't have a domain, 
    the program will not add it in the queue
    """
    companyNameQueue = Queue(size)
    companyDomainQueue = Queue(size)

    """
    Those variables are used to go through the companies on the page, the index is used to get the company at the index
    and the pageCounter is used to know on which page we are
    """
    index = 0
    pageCounter = 0

    fillQueue(companyNameQueue, companyDomainQueue, url, index, pageCounter, size)

    #companyNameQueue.display()
    #companyDomainQueue.display()
    
    """
    Now we have all the informations needed to scrap the companies, we will start to search for the emails of the companies
    and the social network and store it in the class NetworkScrap and EmailScrap and then store it in the class InfoScrap
    """

    """
    Open and initialize the workbook and the worksheet of the workbook
    will write each row with the informations of the companies which time i dequeue the company name and the domain
    """
    wb = Workbook()
    ws = wb.active

    assert ws is not None
    ws.title = tabName

    assert not isinstance(ws, (ReadOnlyWorksheet, Chartsheet))
    ws.append(["Nom de l'entreprise", "Nom de Domain", "Page de Contact", "Facebook", "Twitter", "Linkedin", "Email", "Score du mail", "Pattern de l'email"])

    """
    Open and initialize the csv file with the same informations as the tabsheet
    I also use a csv file to store the informations of the companies, because it's easier to read and to use
    but also can be modified with a text editor
    """
    csvFile = open(f"{csvPath}/{csvFileName}.csv", "w", encoding="utf-8")
    csvFile.write("Nom de l'entreprise, Nom de Domain, Page de Contact, Facebook, Twitter, Linkedin, Email, Score du mail, Pattern de l'email\n")

    data:"list[InfoScrap]" = [] 
    while(not companyNameQueue.is_empty()):
        company_name:str = companyNameQueue.dequeue()
        domain:str = companyDomainQueue.dequeue()
        networkScrap = companyNetwork(domain)


        """
        Email scrap section, we will search for email with the hunter.io API, the API will return the email of the company, a score and a email pattern
        """

        response = requests.get(f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}")
        responseData = response.json()

        """
        Don't process the email & score with the pattern if the API doesn't find any email but find a pattern
        """
        try:
            pattern = responseData['data']['pattern']
        except (IndexError, KeyError):
            pattern = "Non disponible"

        try:
            email = responseData['data']['emails'][0]['value']
            score = 0
        except (IndexError, KeyError):
            emailScrap = None
        else: emailScrap = EmailScrap(email, score)

        if not pattern and not emailScrap:
            print(f"Email not found for {company_name}")

        data.append(InfoScrap(company_name, domain, networkScrap, pattern, emailScrap))
    
    for row in data:
        email = row.email
        if email is None:
            mail = "Non disponible"
            score = "Score non disponible"
        else: 
            mail = email.email
            score = email.score 

        network = row.networkScrap
        if network is None:
            contactPage = "Non disponible"
            facebook = "Non disponible"
            twitter = "Non disponible"
            linkedin = "Non disponible"
        else: 
            if network.contactPage is None: contactPage = "Non disponible"
            else: contactPage = network.contactPage
            if network.facebook is None: facebook = "Non disponible"
            else: facebook = network.facebook
            if network.twitter is None: twitter = "Non disponible"
            else: twitter = network.twitter
            if network.linkedin is None: linkedin = "Non disponible"
            else: linkedin = network.linkedin
        

        ws.append([row.company_name, row.domain, contactPage, facebook, twitter, linkedin, mail, score, row.emailPatern])
        csvFile.write(f"{row.company_name}, {row.domain}, {contactPage}, {facebook}, {twitter}, {linkedin}, {mail}, {score}, {row.emailPatern}\n")
    
    wb.save(f"{tabPath}/{tabFileName}.xlsx")
    csvFile.close()

    messagebox.showinfo("Information", "Le scrap des sociétés est effectué avec succès ! Vous pouvez retrouver les informations dans le fichier companies.xlsx et companies.csv dans le dossier savetab et save respectivement.")
        

    pass #temporary end of the function

def extractFloatFromString(string:str)->float:
    """
    Extract the float from a string, the string must have a number in it
    Allow then to get the number of companies in the region
    """
    return float(''.join(filter(lambda x: x.isdigit() or x == '.', string)))

def fillQueue(nameQueue: Queue, domainQueue: Queue, url:str, index:int, pageCounter:int, maxCompanyCount:int)->None:
    """
    Fill the both queue while they aren't full, must fill the queue only 
    if the company isn't already in the queue and if the company has a domain
    """
    while not nameQueue.is_full():
        """
        Check if we reach the max number of companies available on the page, if it's the case, break the loop
        and exit the function to avoid an error and process with the companies already in the queue
        """
        if pageCounter*index >= maxCompanyCount:
            break

        if index == 0:
            pageCounter += 1
            url = createPageLink(url, pageCounter)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            companies = soup.find_all('tr', class_="MuiBox-root css-1vaqj3c")
        
        """
        Get the relative link of the company page on verif.com and combine it with the base url to get the full link
        """
        companyLink = companies[index].find('a')['href']
        fullLink = "https://www.verif.com" + companyLink

        """
        Check in the page if the company has a domain, if it's the case, add the company name and the domain in the queue
        else pass to the next company
        We only store the company who has a public domain to avoid to search for a contact page 
        """
        response = requests.get(fullLink)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        domainHtmlElement = soup.find('span', class_="MuiTypography-root MuiTypography-bodySmallMedium css-1ymqwc8")

        
        if domainHtmlElement is None:
            index = (index+1)%250
            continue
        domain = domainHtmlElement.text

        domain:str = domainHtmlElement.find('a').text # type: ignore
        
        if not "http://" in domain: Tmpdomain = "http://" + domain
        elif not "https://" in domain : Tmpdomain = "https://"+ domain

        if domain in domainQueue.queue or not verifDNS(domain, Tmpdomain):
            index = (index+1)%250
            continue
            
        """
        The Company name is in the h3 tag in the company page, so we need to get the text in the tag and add it in the queue
        When we add the company name in the queue, we need to add the domain in the domain queue too and then we can pass to the next company
        """
        nameQueue.enqueue(companies[index].find('h3').text.strip())
        domainQueue.enqueue(domain)

        index = (index+1)%250 #The number max of companies on a verif page
    return



def createPageLink(defaultUrl:str, pageCounter:int)->str:
    """
    The first page is the only one who doesn't have a "-page{pageNumber}/" at the end of the url
    Exemple Format : https://www.verif.com/top/revenue-r0/france-rcoun/region-rreg/department-rdep/
    """
    if pageCounter == 1:
        return defaultUrl
    """
    If the isn't the first page of the search, the url isn't same, so we need to add "-page{pageNumber}/"
    at the end of the url, where pageNumber is the number of the page
    Exemple Format with a number of page : https://www.verif.com/top/revenue-r0/france-rcoun/region-rreg/department-rdep-pageN/
    with N the number of the page

    Note : defaultUrl[:-1] is used to remove the last character of the url, in this case, the last "/" to add "-page{pageNumber}/"
    """
    return defaultUrl[:-1] + f"-page{pageCounter}/"


"""
Call the functions in the files network.py and will search the contact page, facebook, twitter and linkedin of the given company
Possibility to add more social network in the future (if needed)
Note : the program cannot find all the informations of the company, because some companies don't have a contact page, or
hide some informations on their website.
Some personal search can be needed to find the informations of the company,if the program doesn't find them

TO-DO: Find a solution for page like "https://cdiscount.com" where i can't scrap any informations
"""
def companyNetwork(domain:str)->"NetworkScrap|None":
    return findNetwork(domain)