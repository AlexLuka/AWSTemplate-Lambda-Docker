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

# Install the specified packages
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 - \
 && export PATH="${POETRY_HOME}/bin:$PATH"    \
 && poetry env use system                     \
 && poetry install --without dev --no-root

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.main.handler" ]