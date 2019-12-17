REM Run MATLAB and share the engine:
matlab -r "matlab.engine.shareEngine"
REM Run PyThesis with matlab flag:
python start.py --project_root %~dp0/example --main_document example --matlab
