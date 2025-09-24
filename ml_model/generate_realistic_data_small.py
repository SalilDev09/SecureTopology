import pandas as pd
import random
import numpy as np

device_types = ['PC', 'Laptop', 'Server', 'Router', 'Switch', 'IoT', 'Printer']
OS_types = ['Windows', 'Linux', 'MacOS', 'RTOS', 'Firmware']

data = []
for i in range(15):
    device = {
        'device_id': f'D{i+1}',
        'firewall': random.choice([0,1]),
        'device_type': random.choice(device_types),
        'OS': random.choice(OS_types),
        'vulnerabilities': np.random.randint(0,50),
        'bandwidth': np.random.randint(10,1000),
        'latency': np.random.randint(1,100)
    }
    device['secure'] = 1 if device['firewall']==1 and device['vulnerabilities']<20 else 0
    data.append(device)

df = pd.DataFrame(data)
df.to_csv('data/realistic_device_data_small.csv', index=False)
print("Dataset created:", df.shape)
