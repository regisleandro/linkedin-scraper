FROM zenika/alpine-chrome:latest AS chrome-base

LABEL name="linkedin-scraper-ai"
LABEL maintener="Regis Leandro Buske - regisleandro@gmail.com"

WORKDIR /app

RUN git clone https://github.com/regisleandro/linkedin-scraper.git .

# Install python dependencies
RUN apk add --no-cache python3 py3-pip

RUN pip3 install -r requirements.txt

RUN useradd -u 1002 -ms /bin/bash user
RUN chown user:user -R /app
USER user

# Expose port for Streamlit app
EXPOSE 8501

# Health check for the application
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start Streamlit app
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
