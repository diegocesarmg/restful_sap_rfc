unzip /sap.zip -d /usr/local && rm -rf /sap.zip
mv nwrfcsdk.conf /etc/ld.so.conf.d
pip install -r requirements.txt