import openai
import typer
from rich import print
from rich.table import Table

import pyttsx3
import speech_recognition as sr

import os
from dotenv import load_dotenv

load_dotenv()

def __textToVoice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    api_key = os.getenv('API_KEY')
    openai.api_key = api_key
    print("🗨️[bold green]Chat GPT api en Python[/bold green]")

    table = Table("Comando", "Descripcion")
    table.add_row("exit", "Salir de la aplicacion")
    table.add_row("new", "Crear nueva conversacion")
    print(table)
    context = {
        "role": "system",
        "content": "You are a helpful assistant."
        }

    messages=[context]

    while True:
        content = __prompt()

        if content=="new":
            print("🗨️ Nueva conversacion ")
            messages=[context]
            content = __prompt()

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response_content = response.choices[0].message.content
        __textToVoice(response_content)

        messages.append({"role": "assistant", "content": response_content})

        print(f"[green][bold green]>[/bold green]{response_content}[/green]")

def __prompt() -> str:
    prompt = typer.prompt("\nSobre que quieres hablar? ")

    if (prompt=="exit"):
        exit = typer.confirm("⚠️ Estas seguro?")
        if exit:
            print("👋 Hasta luego!")
            raise typer.Abort()
        return __prompt()
    return prompt
if __name__ == "__main__":
    typer.run(main)