FROM gitpod/workspace-full:latest

USER gitpod

RUN pip3 install flask flask_cors requests -g