import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv

def configure():
    load_dotenv()

configure()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        description = request.form["description"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(description),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(description):
    return """Podaj gatunek filmu na podstawie zadanego opisu.

Opis: Opowieść o nowojorskiej rodzinie mafijnej. Starzejący się Don Corleone pragnie przekazać władzę swojemu synowi.
Gatunek: Dramat, Gangsterski
Opis: Historia życia Forresta, chłopca o niskim ilorazie inteligencji z niedowładem kończyn, który staje się miliarderem i bohaterem wojny w Wietnamie.
Gatunek: Dramat, Komedia
Opis: Przemoc i odkupienie w opowieści o dwóch płatnych mordercach pracujących na zlecenie mafii, żonie gangstera, bokserze i parze okradającej ludzi w restauracji.
Gatunek: Gangsterski
Opis: Dwóch policjantów stara się złapać seryjnego mordercę wybierającego swoje ofiary według specjalnego klucza - siedmiu grzechów głównych.
Gatunek: Kryminał, Thriller
Opis: Cierpiący na bezsenność mężczyzna poznaje gardzącego konsumpcyjnym stylem życia Tylera Durdena, który jest jego zupełnym przeciwieństwem.
Gatunek: Thriller, Psychologiczny
Opis: Byt ludzkości na Ziemi dobiega końca wskutek zmian klimatycznych. Grupa naukowców odkrywa tunel czasoprzestrzenny, który umożliwia poszukiwanie nowego domu.
Gatunek: Sci-Fi
Opis: Załoga statku kosmicznego Nostromo odbiera tajemniczy sygnał i ląduje na niewielkiej planetoidzie, gdzie jeden z jej członków zostaje zaatakowany przez obcą formę życia.
Gatunek: Horror, Sci-Fi
Opis: {}
Gatunek:""".format(
        description.capitalize()
    )
