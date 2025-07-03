# chatbot-app
A Python application made with CustomTkinter that allows for chatting with chatbots

# Requirements
### Main
- Python 3.11
- Groq API Token *(get a free key here: https://console.groq.com/keys)*
### Libaries
- CustomTkinter 5.2.2
- Pillow 11.3.0
- Groq 0.29.0
### Other
- Assets to replace the placeholder ones
- Set the **GROQ_API_KEY** environmental variable

# Building from source
### Requirements
- PyInstaller
### Limitations
- You need to run the installer on the architecture on which you want the application to run. *(MacOS is an exception: https://pyinstaller.org/en/stable/usage.html#cmdoption-target-architecture)*
- API keys need to be defined in the source code *(e.g.:* <code>groq_client = Groq(api_key="gsk_..."</code>*)* **[temporary until full release]**
- Icons and window names aren't fully supported. (just comment those lines out) **[temporary until full release]**
### Instructions
1. Modify the code as needed to deal with the aforementioned limitations.
2. Run <code>pyinstaller main.py -n APPLICATION_NAME</code> in the directory where the script is located as well as all requirements listed in the first section.
3. Run <code>./dist/APPLICATION_NAME/APPLICATION_NAME</code> or open the file saved at said location to open the application.

# To-Do
### Main
-   Make "Chat History" label stick to the top of the sidebar
-   add settings button on the top right
-   add sidebar toggle in top bar
-   add app name and version in top bar
-   add current chat title as entry, and a "rename" button next to it so the chat can easily be renamed
-   resize messages to fit message size
### Extra
-   add message history for a single chat
-   add some other free api key providers like hugging face or that other one (check in that one discord bot)
-   add chat regeneration button on bot message, and repurpose the button to be used for chat editing on the user message
### Ideas
-   add default system prompts from here: https://github.com/guy915/LLM-System-Prompts
-   provide better installer script
-   package releases built from source
