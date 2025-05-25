# Initial README for ai2c simple registry model project.

# Simple Model Registry

## Overview
This project provides a RESTful API to upload and retrieve metadata of ML models using FastAPI and SQLite.

## How to Run Locally

```bash
git clone https://github.com/echatzip/model-registry.git
cd model-registry
docker-compose up --build

Below are found some of the information needed to show how to execute things locally:

Be aware that this is not battle tested and thus, necessary
modifications might take place.

Until now, all the testing, both on the application and the pipeline
is done locally and therefore, there are some minor details that are
also important between locallly and the remote pipeline.

andromeda:model_registry (main) $ apt show gh
Package: gh
Version: 2.73.0
Priority: optional
Section:
Maintainer: GitHub
Installed-Size: 38.4 MB
Depends: git
Homepage: https://github.com/cli/cli
Download-Size: 14.4 MB
APT-Manual-Installed: yes
APT-Sources: https://cli.github.com/packages stable/main amd64 Packages
Description: GitHub’s official command line tool.
Signed-off-by: Manolic <echatzip@proton.me>

This is a super powerful CLI for most of the operations in github,
remote and local.  However, registration and passkeys must be register
properly.  Without this tool, additional time to debug is needed and is
expensive.

Also, since there was not enough time to debug and deploy the pipeline, the work
has been done locally as shown below:

andromeda:model_registry (main) $ gh extension search act
gh act  nektos/gh-act  v0.2.76
✓  nektos/gh-actions   GitHub CLI Extension to run GitHub actions locally using nek...

Once `git clone'd` the repo, one can execute the pipeline by simply:
`gh extension exec act`

## Flask and Sqlite test locally

Prior on moving on the pipeline

# Github pipeline

The pipeline, as for the latest git commit sha: 0c189088541ab, two steps are to be
executed and are the following:
    - build
    - test

`build` simply prepares the necessary Docker images and deploys the application on the
container.

Step two, `test` is executing some simple smoke tests on the operations requested.  That is,
[POST, GET, GET]

## Flask Application test
The tests which have been successfull locally are executed as follows:
    * docker-compose up --build -- This does all the work on the Docker side where the application
is running.  This allows us to connect to the docker, and debug the application through the following
transactions using curl.

* We need a dummy file to simulate and trick the flask application,.
echo "fake model content" > dummy.pkl

* POST transaction throug curl on "models" file
andromeda:model_registry (main) $ curl -X POST http://localhost:8000/models \\n  \
                    -F "file=@dummy.pkl" \\n  \
                    -F "name=TestModel" \\n   \
                    -F "version=0.1" \\n   \
                    -F "accuracy=0.75"

* GET on models, which indeed returns our "TestMode1"
andromeda:model_registry (main) $ curl -X GET http://localhost:8000/models
[{"accuracy":0.75,"name":"TestModel","timestamp":"2025-05-24T00:24:31.912339","version":"0.1"}]

* Another GET tranaction, but on the endpoint itself, which is as follows:
andromeda:model_registry (main) $ curl -X GET http://localhost:8000/models/TestModel
{"accuracy":0.75,"name":"TestModel","timestamp":"2025-05-24T00:24:31.912339","version":"0.1"}

* Nobody has created the "TestsMode" endpoint, and thus, this use case is correct.
andromeda:model_registry (main) $ curl -X GET http://localhost:8000/models/TestsMode
{"error":"Model not found"}

Therefore, at this time, we do have a simple functional operational registry that we
might place on git.

## First failing Pipeling result.

Tihs demostrates at least, that the `git push` of the PR of ecahtzip has triggered
successfully the pipeline [1].  An email is sent to the author to inform him about
his _failure_ :-).   However, this is my first pipeline from scratch and thus, different
debug methods are happening.

## Flask/Sqlite3 Python source code.

The alternatives for the design of the model registry project as given by the requirements,
were quite a few, but however,  as attempted to explain in the git commit log, the choices
are made for simplicity mostly and the current understanding of the author.

Although FastAPI, as the name suggests, might overcome Flask, the latter is chosen, since
is widely used, and I have had some experience on that quite a few years back and had fewer
things to understand.

When it comes SQLite or PostgreSQL, I wanted to choose the easiest DB since I literally
use a DB in my life :)  Therefore, KISS principle played a huge role in this choice and most
importantly, that the transactions are file oriented (inode based) and I could understand it
easier.  I am not sure, how other SQLs might function.

## TODO

* I have done various attempts, on various steps on the github, and the debugging process
has slowed me down.  That is, `gh exension exec act` is super powerful, there are some env
variables through the "TOKENS" that change the process. Therefore, now that there are two
steps up and running and not working, I'd be able to start iterating both remotely and locally.

* git is used to write history and the start was a little time consuming to gather information
and to start.

* No fault observations are experienced in neither the flask and Sqlite3, which is a good sign.

* Add an "env" file to group variables together for the pipeline.
* Add possible more steps to minimize the errors while working through.
* Add logs and artifacts.
* Update README consisently with appropriate changes.

[1]: https://github.com/echatzip/model-registry/actions/runs/15238987643
