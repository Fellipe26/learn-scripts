
#!/bin/bash

##############################################
#SCRIPT PARA COMPACTAR LOGS DOS MICROSERVICOS#
##############################################

#Mantainer Fellipe Perussatto
echo -e "SCRIPT PRA LIMPAR O FILESYSTEM SETADOS EM DIRECTORIES"
echo
echo
echo -e "VERIFICANDO OS DIRETORIOS..."
echo
echo
echo
echo

#Verifing directories
DIRECTORIES=("/var/lib/docker/volumes/dip_trc/_data/IC/" "/var/lib/docker/volumes/dip_trc/_data/CC/")
echo
echo -e "...DIRETORIOS VERIFICADOS COM SUCESSO"
echo
#Remover arquivos acima de 10 dias
echo "APAGANDO ARQUIVOS A PARTIR DE 5 DIAS ==============>"
for dir in ${DIRECTORIES[@]}; do
        find ${dir} -type f -mtime 5 -exec rm {} \;
done

echo -e "================> ARQUIVOS APAGADOS COM SUCESSO"

#Performing log cleanup.
echo -e "REALIZANDO A COMPACTACAO DOS LOGS"
for dir in ${DIRECTORIES[@]}; do
        LS_DIR=(`ls -ltr ${dir} | awk '{print $9}'`);
                for file in ${LS_DIR[@]}; do
                VALID=$(fuser $DIRECTORIES$file)
                        if [ !$VALID ]; then
                               gzip -9v $DIRECTORIES$file
                        else
                               echo -e "ARQUIVO EM USO"
                        fi
                done
done
echo
echo
echo
echo -e "ARQUIVOS COMPACTADOS COM SUCESSO"
echo
echo
echo
#After compacting, the size of the filesystem will be checked.
echo "TAMANHO ATUAL DOs FILESYSTENS"
echo

for i in ${DIRECTORIES[@]}; do
        du -sh $i
done
