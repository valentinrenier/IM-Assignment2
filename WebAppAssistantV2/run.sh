#!/bin/bash

# Désactiver l'écho des commandes (équivalent de '@echo off' dans Windows)
set +x

# Définir le titre de la fenêtre du terminal (équivalent de 'title')
echo -ne "\033]0;Web App Assistant\007"

# Message de démarrage
echo "Starting Web App Assistant"

# Démarrer le serveur avec http-server sur le port 8082 avec HTTPS
http-server -p 8082 -S -C ./cert.pem -K ./key.pem
