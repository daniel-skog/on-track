
docker run -it --rm --name on-track-backend -v "$PWD"/server:/usr/src/server -w /usr/src/server on-track-backend python main.py && /bin/bash
