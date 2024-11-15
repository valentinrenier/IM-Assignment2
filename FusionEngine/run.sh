#!/bin/bash

# Désactiver l'édition rapide (équivalent de 'quickEdit 2' sur Windows, non applicable sous Linux)
# On peut ignorer cette commande car elle est spécifique à Windows.

# Définir le titre de la fenêtre du terminal (équivalent de TITLE)
echo -ne "\033]0;FUSION\007"

# Exécuter le fichier JAR
java -jar FusionEngine.jar
