# chess
**C**hess **H**igh **E**nd **S**trategy **S**ystem<br><br>
Play against it in your browser with [this](https://github.com/felixwortmann/chess_web)


## File structure
- [**chess_core.ipynb**](./chess_core.ipynb)
  - main minimax, caching, and alpha-beta implementations
- [**play_vs_ai.ipynb**](./play_vs_ai.ipynb)
  - notebook for playing a chess game against the AI with a custom depth
- [**unit_tests.ipynb**](./unit_tests.ipynb)
  - tests for the minimax and evaluation algorithms
- [**requirements.txt**](./requirements.txt)
  - defines dependencies, run with `pip install -r` (tested with python version 3.9.1)
- [**style.css**](./style.css)
  - contains style for jupyter notebooks
- **.logs/**
  - the log files of the played games (will not be pushed to git)
- [**web/***](./web)
  - contains files for a simple web API, not relevant for the AI
- [**Procfile**](./Procfile)
  - needed for automatic deployment of the web API, not relevant for the AI