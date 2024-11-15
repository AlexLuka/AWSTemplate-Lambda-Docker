FROM public.ecr.aws/lambda/python:3.12

# I think that LAMBDA_TASK_ROOT is set to /var/task by default
ARG GITHUB_SHA_ARG

ENV GITHUB_SHA=${GITHUB_SHA_ARG}                \
    POETRY_HOME=${LAMBDA_TASK_ROOT}/poetry      \
    POETRY_VERSION=1.8.4

# Copy requirements.txt
COPY poetry.lock ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}
COPY src/lambda_function ${LAMBDA_TASK_ROOT}/lambda_function

# This will copy all the files from the local 'attachments' directory to
# ${LAMBDA_TASK_ROOT}/attachments
COPY attachments/ ${LAMBDA_TASK_ROOT}/attachments

# Just a sanity check step
# RUN ls -la ${LAMBDA_TASK_ROOT}/attachments

# Install the specified packages
# The first command installs poetry to a docker OS system (not to a Python env)
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 - \
 # Next we set PATH variable to be able to call poetry directly
 && export PATH="${POETRY_HOME}/bin:$PATH"    \
 # Next we need to install all the dependencies to the system Python env.
 # The first command tells that we do not want to create a new environment
 && poetry config virtualenvs.create false --local  \
 # Next we install all the prod dependencies to the system's environment
 && poetry install --without dev

# RUN pip list

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.main.handler" ]