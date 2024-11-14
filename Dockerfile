FROM public.ecr.aws/lambda/python:3.12

# I think that LAMBDA_TASK_ROOT is set to /var/task by default

# Copy requirements.txt
COPY poetry.lock ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}
COPY src/lambda_function ${LAMBDA_TASK_ROOT}/lambda_function

# Install the specified packages
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${LAMBDA_TASK_ROOT}/poetry python3 - \
 && export PATH="${LAMBDA_TASK_ROOT}/poetry/bin:$PATH"    \
 && poetry --version        \
 && poetry env use system                                   \
 && poetry install --without dev

# Copy function code
# COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.main" ]