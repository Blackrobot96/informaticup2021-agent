FROM python
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ./ab_agent.py
ENTRYPOINT ["python", "./ab_agent.py"]