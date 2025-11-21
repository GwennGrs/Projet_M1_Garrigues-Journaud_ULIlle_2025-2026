from iqm.qiskit_iqm import IQMProvider
RESONANCE_API_TOKEN="8Gh0R5Ce4bsagrjhXGrK8ZSz6UamMz2dnfZWsPFzJJ8BmpzbZY94U6VZzKA3EMYH"

provider = IQMProvider("https://cocos.resonance.meetiqm.com/garnet",
            token= input("IQM Resonance token"))
backend = provider.get_backend()
