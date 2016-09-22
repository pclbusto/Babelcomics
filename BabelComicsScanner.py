from ComicBook import *
from ComicBooks import *

from pathlib import Path
import threading
from BabelComicBookManagerConfig import *
import sqlite3


class BabelComicBookScanner():
    def __init__(self, listaDirectorios, listaTipos):
        self.listaDirectorios = listaDirectorios
        self.listaTipos = listaTipos
        self.porcentajeCompletado = 0.0
        self.scanerDir = threading.Thread(target=self.scanearDirtorios)
        self.comics = []

    def countfilesToProces(self):
        cantidad = 0
        listaDirectotiosLocal = [x for x in self.listaDirectorios]
        while (len(listaDirectotiosLocal) > 0):
            valor = listaDirectotiosLocal[0]
            p = Path(listaDirectotiosLocal[0])
            lst = [x for x in p.iterdir() if (x.is_file() and x.name[-3:] in self.listaTipos)]
            cantidad += len(lst)
            dirs = [x for x in p.iterdir() if (x.is_dir())]
            for dir in dirs:
                listaDirectotiosLocal.append(dir)
            listaDirectotiosLocal.remove(valor)
        return (cantidad)

    def scanearDirtorios(self):
        cantidadAProcesar = self.countfilesToProces() * 2
        cantidadProcesada = 0
        while (len(self.listaDirectorios) > 0):
            valor = self.listaDirectorios[0]
            p = Path(self.listaDirectorios[0])
            lst = [x for x in p.iterdir() if (x.is_file() and x.name[-3:] in self.listaTipos)]
            dirs = [x for x in p.iterdir() if (x.is_dir())]
            for item in lst:
                self.comics.append(ComicBook(str(item)))
                cantidadProcesada += 1
            for dir in dirs:
                self.listaDirectorios.append(dir)
            self.listaDirectorios.remove(valor)

            self.porcentajeCompletado = 100 * (cantidadProcesada / cantidadAProcesar)
        ##        conn = sqlite3.connect('BabelComic.db')
        comics = ComicBooks()
        for item in self.comics:
            comics.add(item, False)
            cantidadProcesada += 1
            self.porcentajeCompletado = 100 * (cantidadProcesada / cantidadAProcesar)
        comics.commit()
        comics.close()

    def iniciarScaneo(self):
        self.scanerDir.start()


def testScanning():
    while (manager.scanerDir.isAlive()):
        print(manager.porcentajeCompletado)
    print(manager.porcentajeCompletado)


if __name__ == "__main__":
    config = BabelComicBookManagerConfig()
    manager = BabelComicBookScanner(config.listaDirectorios, config.listaTipos)
    ##    manager.scanearDirtorios()
    ##    print(manager.countfilesToProces())
    manager.iniciarScaneo()
    t = threading.Thread(target=testScanning)
    t.start()
    ##while manager.scanerDir.isAlive():

    ##print(manager.porcentajeCompletado)

##    db = shelve.open('BabelComicsDb-Comics')
##    print(len(db))
##
##    comics = [db[comic] for comic in db]
##    ##print(len(db))
##    ##print(len(comics))
##
##    for comic in comics:
##        print(comic.path,comic.numero)
##    db.close()

