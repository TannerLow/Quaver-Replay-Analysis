REPLAY_PARSER_PROJECT := ./ReplayParser/ReplayParser.csproj
QUAVER_API_PROJECT := ./dependencies/Quaver.API/Quaver.API/Quaver.API.csproj


.PHONY: all clean

all: dependencies dependencies/Quaver.API

dependencies:
	mkdir dependencies

dependencies/Quaver.API:
	@echo [INFO] Cloning $@
	git clone https://github.com/Quaver/Quaver.API.git $@
	dotnet add $(REPLAY_PARSER_PROJECT) reference $(QUAVER_API_PROJECT)
	@echo [INFO] Successfully cloned $@

clean:
	rm -rf ./ReplayParser/bin
	rm -rf ./ReplayParser/obj
