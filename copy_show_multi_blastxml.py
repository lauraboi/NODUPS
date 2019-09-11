#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 11:15:21 2018

@author: diaz
"""

# Import modules
import argparse
from lxml import etree

__author__ = "diaz"
__date__ = "2018/12/05"
__copyright__ = ""
__credits__ = []
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "diaz"
__email__ = ""
__status__ = "Development"


#######################################################################
##                                                                   ##
## Blast_XMLParser Class                                             ##
##                                                                   ##
#######################################################################
class blastx_xmlparser(object):
    """ Procesa la salida outfmt 14 de blastx """

    _PREFIX = {'base':'http://www.ncbi.nlm.nih.gov'}

    ###################################################################
    ##                                                               ##
    ## Encuentra la descripcion de un hit                            ##
    ##                                                               ##
    ###################################################################
    def _hitdescr(self, hit):
        """ Encuentra todas las descripciones de un hit """
        hits_id = list()
        hits_accession = list()
        hits_title = list()
        hits_taxid = list()
        for hitdescr in hit.findall('.//base:HitDescr', self._PREFIX):
            hit_id = hitdescr.find('base:id', self._PREFIX).text
            hits_id.append(hit_id.split('|')[1])
            hit_accession = hitdescr.find('base:accession', self._PREFIX).text
            hits_accession.append(hit_accession)
            #hit_accession = hitdescr.find('base:accession', self._PREFIX).text
            hit_title = hitdescr.find('base:title', self._PREFIX).text
            hits_title.append(hit_title.replace(';', '---'))
            hit_taxid = hitdescr.find('base:taxid', self._PREFIX)
            if (hit_taxid is not None):
                hits_taxid.append(hit_taxid.text)
            else:
                hits_taxid.append('No taxid found')
            #endif
        #endfor
        return hits_taxid, hits_id, hits_accession, hits_title
    #enddef
    ###################################################################
    ##                                                               ##
    ## Muestra la calidad del hit                                    ##
    ##                                                               ##
    ###################################################################
    def _hitquality(self, hit):
        """ Obtiene la calidad del hit """
        #bit_score = float(hit.find('.//base:bit-score', self._PREFIX).text)
        score = int(hit.find('.//base:score', self._PREFIX).text)
        evalue = float(hit.find('.//base:evalue', self._PREFIX).text)
        align_len = int(hit.find('.//base:align-len', self._PREFIX).text)
        #gaps = int(hit.find('.//base:gaps', self._PREFIX).text)
        return [score, evalue, align_len]
    #enddef

    ###################################################################
    ##                                                               ##
    ## Constructor de la clase.                                      ##
    ##                                                               ##
    ###################################################################
    def __init__(self, xml, nohits=True):
        """ Inicializa el objeto e imprime el resultado """
        # Mostrar no-hits?
        self.nohits = nohits
        # Procesa el fichero xml
        tree = etree.parse(xml)
        # Procesa los tags xi:include y reconstruye el documento final
        tree.xinclude()
        root = tree.getroot()

        # Fichero de salida
        name = xml.split(".")[-2].split("/")[-1] + ".csv"
        out = open(name, "w")

        out.write("taxid;gi;accession;title;evalue;query-title;num;go;num-go\n")

        # Para cada Search:
        for search in root.findall('.//base:Search', self._PREFIX):
            #query_id = search.find('base:query-id', self._PREFIX).text
            query_title = search.find('base:query-title', self._PREFIX).text
            # Comprueba si se encuentra un hit
            message = search.find('base:message', self._PREFIX)
            if (message is not None):
                # No hay hits
                if (self.nohits):
                    #print('[%s] %s' % (query_title))
                    print()
                    #print("**** %s" % message.text)
                    #print()
                    #print('[End %s]' % query_id)
                    #print()
                #endif
            else:
                # Busca todos los Hits
                # print query-tittle
                for hit in search.findall('.//base:Hit', self._PREFIX):
                    hit_num = hit.find('base:num', self._PREFIX).text
                    # print num

                    # Busca las descripciones del Hit
                    hits_taxid, hits_id, hits_accession, hits_title = \
                        self._hitdescr(hit)

                    # Obtiene información con la calidad del Hit
                    qual = self._hitquality(hit)

                    for i in range(len(hits_taxid)):
                        out.write("%s;%s;%s;%s;%s;%s;%s;;\n" % \
                              (hits_taxid[i], hits_id[i], \
                               hits_accession[i], hits_title[i], \
                               qual[1], query_title, hit_num))
                    #endfor
                #endfor
                #print('[End %s]' % query_id)
            #endif
        #endfor
        out.close()
    #enddef
#endclass

#######################################################################
## Procesa los argumentos                                            ##
#######################################################################
def get_options():
    # Arguments
    parser = argparse.ArgumentParser(
        description='Genera un resumen de los resultados de blastx'
    )
    parser.add_argument(
        'xmlfile',
        action='store',
        help='Fichero generado por blastx'
    )
    parser.add_argument(
        '-n', '--nohits',
        action='store_true',
        help='Show/not show no-hits'
    )

    # Parse --ini argument
    args = parser.parse_args()
    return args
#enddef

#######################################################################
##                                                                   ##
## Main program                                                      ##
##                                                                   ##
#######################################################################
if __name__ == "__main__":
    #
    # Parametros
    args = get_options()
    xmlfile = args.xmlfile
    nohits = args.nohits

    bp = blastx_xmlparser(xmlfile, nohits=nohits)

#endif

