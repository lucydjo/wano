# wano/main.py

import argparse
import os
from flask import Flask, send_file, render_template, request
from pyngrok import ngrok
import requests
import uuid

app = Flask(__name__,
    static_url_path='/assets', 
    static_folder='static',
    template_folder='templates')

def main():
    parser = argparse.ArgumentParser(description='Description of your command')
    parser.add_argument('file_name', help='Name of the file to broadcast')
    parser.add_argument('--port', type=int, default=5000, help='Port number for Flask server')
    args = parser.parse_args()

    # Chemin absolu du fichier en fonction du répertoire où le script est lancé
    script_dir = os.getcwd()

    file_path = os.path.join(script_dir, args.file_name)

    # Configure ngrok avec votre token d'authentification
    try:
        ngrok.set_auth_token(os.getenv('NGROK_WANO_KEY'))
    except:
        print('ngrok auth key not found. use : export NGROK_WANO_KEY=your_ngrok_auth_key')
        exit()

    secret_key = str(uuid.uuid4())

    # Démarrer le tunnel ngrok pour exposer le serveur Flask
    tunnel = ngrok.connect(args.port)
    public_url = tunnel.public_url
    print(f'ngrok URL: {public_url}/{secret_key}')

    @app.route('/save/<secret>', methods=['POST'])
    def save_file(secret):
        if secret != secret_key:
            return 'Invalid secret key'
        try:
            content = request.form['content']
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(content)
            return 'File saved !'
        except Exception as e:
            return str(e)

    @app.route('/read/<secret>', methods=['POST'])
    def read_file(secret):
        if secret != secret_key:
            return 'Invalid secret key'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                content = file.read()
            return content
        except Exception as e:
            return str(e)

    @app.route('/<secret>')
    def serve_file(secret):
        if secret != secret_key:
            return 'Invalid secret key'
        return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Wano Editor</title>
    <!-- Inclure les fichiers CSS de CodeMirror -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.css" integrity="sha512-uf06llspW44/LZpHzHT6qBOIVODjWtv4MxCricRxkzvopAlSWnTf6hpZTFxuuZcuNE9CBQhqE0Seu1CoRk84nQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/theme/pastel-on-dark.min.css" integrity="sha512-kcwXu8swgWHAdTrmVuUiuJK0+VtDCVXhOpznpnZHfx84G78aGLqbEtu5MYN08zV3XpP719SPTOzrcfirU1JnDA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js" integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jersey+25&display=swap" rel="stylesheet">
    <style>
        html { background: #2C2827; }
        .CodeMirror { 
          width: 100%;
          height: 100%;
          position: absolute;
          top: 40px;
          left: 0;
        }
        .cm-s-pastel-on-dark.CodeMirror {
            color: #fff;
            line-height: 1.5;
        }
        .infos {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 40px;
            background: #34302f;
            color: #FFF;
            padding: 10px;
            font-family: "Jersey 25", sans-serif;
            font-weight: 400;
            font-style: normal;
        }
    </style>
</head>
<body>
    <div class="infos">Wano 0.5 | Use Ctrl+S to save</div>
    <textarea id="myTextarea">Text is loading.. Do not save now !</textarea>

    <!-- Inclure le fichier JavaScript de CodeMirror -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.js" integrity="sha512-8RnEqURPUc5aqFEN04aQEiPlSAdE0jlFS/9iGgUyNtwFnSKCXhmB6ZTNl7LnDtDWKabJIASzXrzD0K+LYexU9g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

    <!-- Script JavaScript pour initialiser CodeMirror -->
    <script>
        // Récupérer la référence à la textarea
        var textarea = document.getElementById('myTextarea');

        // Initialiser CodeMirror avec la textarea
        var editor = CodeMirror.fromTextArea(textarea, {
            lineNumbers: true, // Afficher les numéros de ligne
            theme: 'pastel-on-dark' // Utiliser le thème par défaut (vous pouvez en choisir d'autres)
        });

        $.post( "/read/'''+secret_key+'''" )
        .done(function( data ) {
            editor.setValue(data);
        });

        // Ajuster la taille de l'éditeur CodeMirror lors du redimensionnement de la fenêtre
        window.addEventListener('resize', function() {
            editor.setSize('90%', '90%'); // Ajuster la taille de l'éditeur pour qu'il remplisse 90% de la fenêtre
        });

        // Gérer l'événement de pression des touches
        document.addEventListener('keydown', function(event) {
            // Vérifier si la combinaison de touches Ctrl + S est enfoncée
            if (event.ctrlKey && event.key === 's') {
                event.preventDefault(); // Empêcher le comportement par défaut (sauvegarde de fichier)

                // Récupérer le contenu de l'éditeur CodeMirror
                var content = editor.getValue();

                $.post( "/save/'''+secret_key+'''", { "content": content })
                .done(function( data ) {
                  Swal.fire(data);
                });
            }
        });
    </script>
</body>
</html>


'''

    # Démarrer le serveur Flask
    app.run(port=args.port)

if __name__ == "__main__":
    main()
