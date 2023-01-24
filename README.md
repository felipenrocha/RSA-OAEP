# RSA Signature Generator/Verifier

Author: Felipe Nacimento Rocha


    TODO:

        1. Parte I: Geração de chaves e cifra
        
                a. Geração de chaves (p e q primos com no mínimo de 1024 bits)
                b. Cifração/decifração assimétrica RSA usando OAEP.
    
    
        2.  Parte II: Assinatura
        
                a. Cálculo de hashes da mensagem em claro (função de hash SHA-3)
                b. Assinatura da mensagem (cifração do hash da mensagem)
                c. Formatação do resultado (caracteres especiais e informações para verificação em BASE64)
        
        
        3. Parte III: Verificação:
        
                a. Parsing do documento assinado e decifração da mensagem (de acordo com a formatação usada, no caso BASE64)
                b. Decifração da assinatura (decifração do hash)
                c. Verificação (cálculo e comparação do hash do arquivo)


