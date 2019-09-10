#!/bin/bash

function usage()
# Funcion que establece los parametros necesarios para ejecutar el programa
{
    echo "Script que ejecuta el pipeline completo de anotacion con terminos GO y"
    echo "visualización para una muestra. La entrada es el fichero comprimido"
    echo "con los resultados de la anotacion del BLASTx"
    echo ""
    echo -e "\t-h --help\tMuestra esta ayuda"
    echo -e "\t-F --file\tNombre del fichero .tar.gz con los resultados de blastx"
    echo -e "\t-P --path\tRuta al directorio que contiene el fichero .tar.gz"
    echo -e "\t-D --dir\tRuta al directorio que contiene los scripts del pipeline"
    echo ""
}

for i in "$@"; do
    echo "$i"
    case $i in
        -h=* | --help)
            usage
            exit
            ;;
        -F=* | --file)
            FILE="${i#*=}"
            ;;
        -P=* | --path)
            WPATH="${i#*=}"
            ;;
        -D=* | --dir)
            DIR="${i#*=}"
            ;;
        *)
            echo "***ERROR: unknown parameter $i***"
            echo ""
            usage
            exit 1
            ;;
    esac
    shift
done

# Pasos Previos

cd $WPATH

name=${FILE%.tar.gz}

xml=${name}/results


# Se crea un nuevo directorio y se descomprime el fichero de los resultados de BLASTx
new_dir=${name}_csv

mkdir $new_dir

tar -xzvf $FILE


## PASO 1
cd ${WPATH}/${xml}

# Se ejecuta el programa que procesa los XML y los transforma a formato CSV
for f in $(ls *.out)
do
    $DIR/copy_show_multi_blastxml.py $f
    mv ${f%.*}.csv ${WPATH}/${new_dir}
done



## PASO 2.A
cd ${WPATH}/${new_dir}

file_all=${name}_all.csv

# Se unen todos los CSV de una misma muestra y se realiza el mapeo
cat $WPATH/${new_dir}/* > $file_all

$DIR/query_join.py $file_all


## PASO 2.B.1
# Se indica la ruta de la base de datos nr
export BLASTDB=$DIR/DB/nr

# Se lee el fichero con todos los resultados y para cada GI se obtiene
# una secuencia FASTA
while read line
do
    gi=`echo "$line" | cut -d';' -f 2`
    if [ $gi != 'gi' ]
    then
	blastdbcmd -entry "$gi" -db nr -outfmt "%f" >> $name".fasta"
    fi
done  < $file_all


## PASO 2.B.2
# Se realiza la anotación de las secuencias FASTA con InterProScan
$DIR/my_interproscan/interproscan-5.32-71.0/interproscan.sh -i \
	$name".fasta" -f tsv -o $name"_interpro.tsv" -goterms

## PASO 3
# Se unen las dos anotaciones
$DIR/unir.py $name"_interpro.tsv" $file_all

## PASO 4
# Se crea el grafo a partir de todos los GO anotados a la muestra
$DIR/grafo.py $name"_soloGO.txt"
