# chatcli

Usage

```bash
git clone git@github.com:ehrlich-b/chatcli.git
cd chatcli
echo "OPENAI_KEY=<your key>" > .env
poetry install
poetry run python main.py
```

If you have access to gpt-4 you can pass the -4 flag to use it instead of gpt-3.

```bash
poetry run python main.py -4
```

