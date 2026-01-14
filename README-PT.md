<div align="center">
  
![AWS Route 53](https://img.icons8.com/color/96/amazon-web-services.png)

# Toolkit de Auditoria e Habilitação DNSSEC para Route53

**Atualizado: 14 de Janeiro de 2026**

[![Follow @nicoleepaixao](https://img.shields.io/github/followers/nicoleepaixao?label=Follow&style=social)](https://github.com/nicoleepaixao)
[![Star this repo](https://img.shields.io/github/stars/nicoleepaixao/route53-dnssec-audit?style=social)](https://github.com/nicoleepaixao/route53-dnssec-audit)
[![Medium Article](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://nicoleepaixao.medium.com/)

<p align="center">
  <a href="README-PT.md">🇧🇷</a>
  <a href="README.md">🇺🇸</a>
</p>

</div>

---

<p align="center">
  <img src="img/route53-dnssec-audit-and-enablement.png" alt="dnssec Architecture" width="1800">
</p>

## **Visão Geral**

Este repositório fornece um toolkit completo para auditar zonas DNS através de múltiplas contas AWS e habilitar DNSSEC para todas as zonas públicas elegíveis do Route 53. O toolkit inclui scripts automatizados de inventário, avaliação de elegibilidade DNSSEC, verificação de registrador e guias operacionais abrangentes para deployment seguro de DNSSEC.

---

## **Informações Importantes**

### **O Que Este Toolkit Faz**

| **Aspecto** | **Detalhes** |
|------------|-------------|
| **Automação de Inventário** | Enumera todas as zonas hospedadas do Route 53 através de contas |
| **Classificação de Zonas** | Detecta zonas públicas vs privadas automaticamente |
| **Status DNSSEC** | Recupera status de assinatura atual (assinado/não assinado/não suportado) |
| **Detecção de Registrador** | Identifica domínios Route53 vs registrador externo |
| **Formato de Exportação** | Relatório CSV com análise detalhada |
| **Modo de Operação** | Somente-leitura, impacto zero na infraestrutura existente |

### **Por Que DNSSEC Importa**

DNSSEC (Domain Name System Security Extensions) adiciona assinaturas criptográficas aos registros DNS, prevenindo:

- **Envenenamento de Cache**: Injeção maliciosa de registros DNS
- **Ataques Man-in-the-Middle**: Interceptação de consultas DNS
- **DNS Spoofing**: Respostas DNS fraudulentas
- **Sequestro de Domínio**: Takeovers não autorizados de domínio

### **Benefícios da Solução**

✅ **Suporte Multi-Conta**: Escaneie todas as contas AWS de um único script  
✅ **Compatível com Registrador Externo**: Funciona com Registro.br, GoDaddy, Cloudflare e mais  
✅ **Zero Risco**: Operações somente-leitura, sem modificações  
✅ **Relatórios Abrangentes**: Exportação CSV pronta para auditorias de segurança  
✅ **Pronto para Produção**: Guia completo de habilitação incluído

---

## **Como Funciona**

### **Fluxo do Processo**

1. **Autenticação:** Conecta a contas AWS usando perfis configurados
2. **Descoberta:** Enumera todas as zonas hospedadas do Route 53
3. **Classificação:** Identifica zonas públicas vs privadas
4. **Verificação de Status:** Recupera status atual de assinatura DNSSEC
5. **Detecção de Registrador:** Determina se o domínio está no Route53 ou registrador externo
6. **Exportação:** Gera relatório CSV com análise completa

### **Proteção DNSSEC**

Route 53 suporta assinatura DNSSEC gerenciada, onde a AWS gerencia:

- **Criação de Chaves**: KSK (Key Signing Key) e ZSK (Zone Signing Key) automáticas
- **Ciclo de Vida de Chaves**: Rotação e gerenciamento automatizados
- **Rollover**: Atualizações de chaves perfeitas
- **Assinatura de Registros**: Assinaturas criptográficas para todos os registros DNS

**Importante:** O registrador de domínio deve suportar registros DS DNSSEC. Para domínios `.br` (Registro.br), isso é totalmente suportado.

---

## **Componentes Disponíveis**

<div align="center">

| **Componente** | **Propósito** | **Formato** |
|:-------------:|:-----------:|:----------:|
| **Script de Inventário** | Escaneamento automatizado de zonas | Python 3.x |
| **Relatório CSV** | Exportação de análise detalhada | CSV |
| **Guia de Habilitação** | Setup DNSSEC passo a passo | Markdown |
| **Doc de Troubleshooting** | Problemas comuns e soluções | Markdown |

</div>

---

## **Como Começar**

### **1. Clonar Repositório**

```bash
git clone https://github.com/nicoleepaixao/route53-dnssec-audit-and-enablement.git
cd route53-dnssec-audit-and-enablement
```

### **2. Instalar Dependências**

```bash
pip install -r src/requirements.txt
```

**requirements.txt:**
```text
boto3
botocore
```

### **3. Configurar Perfis AWS**

Certifique-se de que seus perfis AWS estão configurados em `~/.aws/config`:

```ini
[profile pamcard-dev]
region = us-east-1

[profile roadcard]
region = us-east-1

[profile pamcard-predev]
region = us-east-1
```

### **4. Executar Script de Inventário**

```bash
cd src/
python3 route53_dnssec_inventory.py
```

**Saída:** `output/route53_dnssec_inventory.csv`

**Nota:** O script executa operações somente-leitura e não modifica nenhuma configuração do Route 53.

---

## **Executando o Inventário**

1. **Executar Script:** Navegue até o diretório `src/` e execute o script Python
   ```bash
   python3 route53_dnssec_inventory.py
   ```

2. **Monitorar Progresso:** O script escaneará todos os perfis AWS configurados

3. **Revisar Saída:** Arquivo CSV gerado no diretório `output/`

4. **Analisar Resultados:** Abra o CSV no Excel ou qualquer ferramenta de planilha

5. **Planejar Habilitação:** Identifique zonas com status `UNSIGNED` para deployment DNSSEC

---

## **Entendendo a Saída**

### **Estrutura do Relatório CSV**

| profile     | account_id | hosted_zone_id | domain_name            | zone_type | registered_in_route53 | dnssec_status                 |
|-------------|-------------|----------------|-------------------------|-----------|------------------------|-------------------------------|
| prod        | 111111111111 | ZABC123XYZ001  | api.company.com         | PUBLIC    | NO                     | UNSIGNED                      |
| staging     | 222222222222 | ZXYZ987ABC002  | staging.company.com     | PUBLIC    | NO                     | UNSIGNED                      |
| dev         | 333333333333 | ZAAA111BBB003  | dev.company.internal    | PRIVATE   | NO                     | NOT_SUPPORTED_PRIVATE_ZONE    |
| qa          | 444444444444 | Z456XYZ123444  | qa.company.com          | PUBLIC    | NO                     | NOT_CONFIGURED                |
| network     | 555555555555 | ZNET123ZONE55  | corpnet.internal.local  | PRIVATE   | NO                     | NOT_SUPPORTED_PRIVATE_ZONE    |

### **Descrição dos Campos**

| **Campo** | **Descrição** |
|-----------|----------------|
| **profile** | Perfil AWS CLI usado para escaneamento |
| **account_id** | Identificador da conta AWS |
| **hosted_zone_id** | ID da zona hospedada do Route 53 |
| **domain_name** | Nome de domínio totalmente qualificado |
| **zone_type** | PUBLIC (elegível) ou PRIVATE (não suportado) |
| **registered_in_route53** | YES se domínio registrado no Route53 Domains |
| **dnssec_status** | SIGNED, UNSIGNED, ou NOT_SUPPORTED_PRIVATE_ZONE |

### **Elegibilidade DNSSEC**

- **Zonas públicas** → Elegíveis para DNSSEC
- **Zonas privadas** → Explicitamente não suportadas
- **Domínios de registrador externo** → Requerem configuração de registro DS no registrador

---

## **Guia de Habilitação DNSSEC**

### **Passo 1: Identificar Zonas Elegíveis**

Filtre o relatório CSV por:

- `zone_type == PUBLIC`
- `dnssec_status == UNSIGNED`

Essas zonas são elegíveis para DNSSEC e prontas para habilitação.

### **Passo 2: Habilitar Assinatura DNSSEC no Route 53**

1. **Console AWS** → Route 53 → Hosted Zones → Selecione seu domínio
2. Navegue até: **DNSSEC signing** → **Enable DNSSEC**
3. A AWS irá automaticamente:
   - Habilitar assinatura de chave gerenciada pelo route-53
   - Criar uma KSK dentro do AWS KMS
   - Começar a assinar todos os registros DNS

### **Passo 3: Recuperar o Registro DS**

Após habilitar DNSSEC:

1. Route 53 → Hosted Zone → DNSSEC → **DS Records**
2. Copie os valores do registro DS:

```text
Key Tag: 2371
Algorithm: 13
Digest Type: 2
Digest: 48FD8DE2349F3AA3AA3C09B7E0...
```

### **Passo 4: Publicar Registro DS no Registrador**

#### **Para Domínios Registro.br:**

1. Acesse https://registro.br
2. Selecione seu domínio
3. Navegue até a seção **DNSSEC**
4. Insira os valores do Registro DS:
   - Key Tag
   - Algorithm
   - Digest Type
   - Digest
5. Salve as mudanças

#### **Para Outros Registradores:**

- **GoDaddy**: Domain Settings → Advanced Settings → DNSSEC
- **Cloudflare**: DNS → Settings → DNSSEC
- **HostGator**: Domain Management → DNSSEC Settings

### **Passo 5: Validar Propagação DNSSEC**

**Usando comando dig:**

```bash
dig +dnssec seudominio.com.br
```

Procure pela flag `ad` (Authenticated Data) na resposta.

**Usando validadores online:**

- [DNSViz](https://dnsviz.net/)
- [Verisign DNSSEC Debugger](https://dnssec-debugger.verisignlabs.com/)

**Nota:** A propagação pode levar até 48 horas.

---

## **Registradores Suportados**

| **Registrador** | **Suporte DNSSEC** | **Configuração** |
|---------------|-------------------|-------------------|
| Registro.br | ✅ Suporte Completo | Interface web com entrada de registro DS |
| GoDaddy | ✅ Suporte Completo | Configurações de domínio → Avançado |
| Cloudflare | ✅ Suporte Completo | Painel de configurações DNS |
| HostGator | ✅ Suporte Completo | Console de gerenciamento de domínio |
| Google Domains (legacy) | ✅ Suporte Completo | Configurações de domínio |

---

## **Troubleshooting**

### **Problemas Comuns**

| **Problema** | **Causa** | **Solução** |
|-----------|-----------|--------------|
| Registro DS rejeitado | Tipo de digest incompatível ou erro de cópia | Verifique se todos os campos correspondem exatamente |
| Flag AD não retornada | Propagação em andamento | Aguarde até 48 horas, verifique novamente |
| Erro de zona privada | DNSSEC não suportado para zonas privadas | Habilite apenas para zonas públicas |
| Registrador não suportado | Registrador não suporta DNSSEC para TLD | Contate suporte do registrador |
| Erro de permissão KMS | Role IAM não tem permissões KMS | Adicione permissão `kms:CreateKey` |

### **Comandos de Validação**

```bash
# Verificar status DNSSEC
dig +dnssec +multi example.com

# Consultar tipo de registro específico
dig +dnssec example.com DNSKEY

# Verificar registro DS na zona pai
dig +dnssec example.com DS

# Rastrear cadeia DNSSEC completa
dig +dnssec +trace example.com
```

---

## **Funcionalidades**

| **Funcionalidade** | **Descrição** |
|-------------|-----------------|
| **Escaneamento Multi-Conta** | Enumera zonas através de todos os perfis AWS |
| **Classificação de Zonas** | Detecção automática público/privado |
| **Status DNSSEC** | Recuperação de status de assinatura em tempo real |
| **Detecção de Registrador** | Identifica domínios Route53 vs externos |
| **Exportação CSV** | Relatório detalhado para auditorias e compliance |
| **Impacto Zero** | Somente-leitura, sem mudanças na infraestrutura |
| **Suporte Registrador Externo** | Funciona com Registro.br, GoDaddy, Cloudflare |
| **Documentação Abrangente** | Guias completos de habilitação e troubleshooting |

---

## **Casos de Uso**

Este toolkit é ideal para:

- **Auditorias de Segurança**: Avaliação abrangente de compliance DNSSEC
- **Migração Cloud**: Baseline de segurança DNS pré-migração
- **Requisitos de Compliance**: Atender padrões de segurança da indústria (PCI-DSS, SOC 2)
- **Governança Multi-Conta**: Gerenciamento centralizado de segurança DNS
- **Mitigação de Riscos**: Prevenir ataques baseados em DNS através de todos os domínios
- **Hardening de Infraestrutura**: Fortalecer postura geral de segurança AWS

---

## **Tecnologias Utilizadas**

| **Tecnologia** | **Versão** | **Propósito** |
|----------------|-------------|-------------|
| Python | 3.8+ | Script principal e automação |
| boto3 | Mais recente | SDK AWS para chamadas API Route 53 |
| botocore | Mais recente | Acesso de baixo nível a serviços AWS |
| AWS Route 53 | - | Serviço DNS e gerenciamento DNSSEC |
| AWS KMS | - | Gerenciamento de chaves para assinatura DNSSEC |
| AWS CLI | Mais recente | Gerenciamento de perfis e credenciais |

---

## **Estrutura do Projeto**

```text
route53-dnssec-audit-and-enablement/
│
├── README.md                          # Documentação completa do projeto
│
├── src/
│   ├── route53_dnssec_inventory.py   # Script principal de inventário
│   └── requirements.txt               # Dependências Python
│
├── output/
│   └── route53_dnssec_inventory.csv  # Relatório de inventário auto-gerado
│
├── docs/
│   ├── dnssec_enablement_guide.md    # Passos completos de habilitação DNSSEC
│   └── troubleshooting.md            # Problemas comuns e resoluções
│
└── .gitignore                         # Arquivos ignorados (output/, *.csv, .env)
```

---

## **Informações Adicionais**

Para mais detalhes sobre DNSSEC, segurança Route 53 e melhores práticas DNS, consulte:

- [AWS Route 53 DNSSEC Documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec.html) - Guia oficial
- [DNSSEC How It Works](https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en) - Explicação ICANN
- [Registro.br DNSSEC Guide](https://registro.br/tecnologia/dnssec.html) - Domínios brasileiros
- [DNSViz Visualization Tool](https://dnsviz.net/) - Validação DNSSEC

---

## **Conecte-se & Siga**

Mantenha-se atualizado com automação de segurança AWS e melhores práticas DNS:

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nicoleepaixao)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white&style=for-the-badge)](https://www.linkedin.com/in/nicolepaixao/)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@nicoleepaixao)

</div>

---

## **Aviso Legal**

Este toolkit é fornecido para propósitos de auditoria de segurança DNS e habilitação DNSSEC. Configuração DNSSEC, compatibilidade de registrador e tempos de propagação podem variar. Sempre teste habilitação DNSSEC em ambientes de não-produção antes de implantar em domínios de produção. Consulte a documentação oficial da AWS e seu registrador de domínio para informações mais atuais.

---

<div align="center">

**Proteja sua infraestrutura DNS com segurança!**

*Documento Criado: 5 de Dezembro de 2025*

Made with ❤️ by [Nicole Paixão](https://github.com/nicoleepaixao)

</div>
