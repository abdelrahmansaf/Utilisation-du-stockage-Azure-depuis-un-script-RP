import sys
import argparse
import configparser
import logging
import os.path
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient




logging.basicConfig(
    filename="log_main.log",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',)




"""
Liste les blobs du contenuer indiqué.
"""
def listb(args, containerclient):
    blob_list=containerclient.list_blobs()
    for blob in blob_list:
        print(blob.name)

"""
Charge le blob dans le contenur du client.
"""
def upload(cible, blobclient):
    with open(cible, "rb") as f:
        blobclient.upload_blob(f)

""" 
Téléchager le blob et le place dans le dossier créé
"""
def download(filename, dl_folder, blobclient):
    with open(os.path.join(dl_folder,filename), "wb") as my_blob:
        blob_data=blobclient.download_blob()
        blob_data.readinto(my_blob)

'''
Permet la connexion au client  pour configurer les propriétés du compte
'''
def main(args,config):
    logging.info("lancement la function main")
    blobclient=BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    logging.debug("connection u compte storage")

    containerclient=blobclient.get_container_client(config["storage"]["container"])
    logging.debug("connection au container")
    if args.action=="list":
        logging.debug('lancement la function list')
        return listb(args, containerclient)
    else:
        if args.action=="upload":
            
            blobclient=containerclient.get_blob_client(os.path.basename(args.cible))
            logging.debug('lancement la function upload')
            loggi.warning('uploading')
            return upload(args.cible, blobclient)
        elif args.action=="download":
            logging.debug('lancement la function upload')
            blobclient=containerclient.get_blob_client(os.path.basename(args.remote))
            loggi.warning('dowloading')
            return download(args.remote, config["general"]["restoredir"], blobclient)
    

if __name__=="__main__":
    parser=argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument("-cfg",default="config.ini",help="chemin du fichier de configuration")
    parser.add_argument("-lvl",default="info",help="niveau de log")
    subparsers=parser.add_subparsers(dest="action",help="type d'operation")
    subparsers.required=True
    
    parser_s=subparsers.add_parser("upload")
    parser_s.add_argument("cible",help="fichier à envoyer")

    parser_r=subparsers.add_parser("download")
    parser_r.add_argument("remote",help="nom du fichier à télécharger")
    parser_r=subparsers.add_parser("list")


    args=parser.parse_args()

    #erreur dans logging.warning : on a la fonction au lieu de l'entier
    loglevels={"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
    print(loglevels[args.lvl.lower()])
    logging.basicConfig(level=loglevels[args.lvl.lower()])

    config=configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args,config))
