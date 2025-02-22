FROM kalilinux/kali-rolling
FROM python:3.10.0-slim
RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-pip && \
    pip install sublist3r && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    inetutils-ping \
    whois \
    dnsrecon \
    curl \
    netcat \
    telnet \
    whatweb \
    sqlmap \
    hashcat \
    git \
    golang \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Subfinder
RUN git clone https://github.com/projectdiscovery/subfinder.git /opt/subfinder && \
    cd /opt/subfinder/v2/cmd/subfinder && \
    go mod tidy && \
    go build && \
    mv subfinder /usr/local/bin/ && \
    rm -rf /opt/subfinder

#RUN git clone https://github.com/screetsec/Kuro.git /opt/Kuro && \
#    chmod +x /opt/Kuro/kuro.sh


WORKDIR /app
COPY . .

RUN chmod +x /app/my_script.sh
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8000"]