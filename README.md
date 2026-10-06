# Blender Product Fidelity

Skill para Codex orientada à modelagem, aos materiais e à validação de produtos no Blender a partir de referências. O foco é fidelidade verificável: proporções, detalhes construtivos, branding, iluminação, render, animação e derivados para tempo real.

A skill orienta o trabalho do Codex. Ela não instala o Blender e não transforma uma única foto em geometria verificada de todos os lados.

## Instalação pelo Codex

Com o Codex aberto, envie:

```text
Use $skill-installer para instalar a skill do repositório gilberto-insany/blender-product-fidelity, caminho skills/blender-product-fidelity, branch main. Instale a pasta completa, incluindo references, scripts e agents. Se já existir uma instalação, preserve-a e confirme comigo antes de substituí-la.
```

A skill fica disponível a partir do próximo turno. Para uma instalação reproduzível de uma versão específica, informe também o SHA completo do commit desejado como `--ref` ao instalador; a branch `main` acompanha atualizações.

## Instalação manual no macOS ou Linux

É necessário ter Git. Clone o repositório e copie a pasta completa, sem sobrescrever uma instalação existente:

```bash
git clone https://github.com/gilberto-insany/blender-product-fidelity.git
cd blender-product-fidelity
# Para fixar uma versão, execute: git checkout --detach SHA_COMPLETO_DO_COMMIT
git rev-parse HEAD
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
if [ -e "$skill_root/blender-product-fidelity" ]; then
  printf '%s\n' 'Já existe uma instalação. Preserve-a antes de atualizar.' >&2
else
  mkdir -p "$skill_root"
  cp -R skills/blender-product-fidelity "$skill_root/"
fi
```

Guarde o SHA exibido por `git rev-parse HEAD` para reinstalar a mesma versão. No Windows, prefira o instalador do Codex; os comandos de shell acima são destinados ao macOS e Linux.

## Requisitos e controle do Blender

- Codex com suporte a skills e acesso autorizado ao computador ou ambiente onde o Blender será executado.
- Blender instalado separadamente. Os scripts usam o módulo `bpy` e devem ser executados pelo Python do Blender, não por um Python comum.
- Referências e ativos que você tenha direito de usar: fotos, dimensões, desenhos, logotipos, fontes e texturas.
- O caminho principal usa Blender Python em modo background. Configure `BLENDER_BIN` com o executável real do seu sistema. No macOS, o caminho comum é `/Applications/Blender.app/Contents/MacOS/Blender`; no Linux, pode ser `blender` no PATH.
- O Blender Toolkit é uma integração opcional de controle ao vivo, não incluída neste pacote. A skill não instala, habilita nem inicia um servidor automaticamente. Se ele não estiver disponível, use o fluxo Blender Python. Leia `references/live-toolkit.md` antes de usá-lo.

Antes de executar scripts em arquivos reais, preserve o `.blend` original e use saídas versionadas. O helper de render altera a configuração da cena carregada, pode salvar uma cópia quando solicitado e grava a imagem de saída; escolha caminhos novos.

## Como usar

```text
Use $blender-product-fidelity para reconstruir este produto a partir das referências anexadas. Comece pelas proporções e pela câmera. Preserve o arquivo original e mostre um preview antes do render final.
```

```text
Use $blender-product-fidelity para revisar a geometria e os materiais deste .blend. Não renderize ainda. Aponte o que foi verificado e o que depende de novas referências.
```

```text
Use $blender-product-fidelity para preparar uma animação de produto. Faça primeiro um benchmark autorizado e estime o custo da sequência antes de iniciar o render completo.
```

## Conteúdo

A pasta instalável é `skills/blender-product-fidelity/`. Mantenha `SKILL.md`, `agents/`, `references/` e `scripts/` juntos. Não basta copiar apenas o arquivo `SKILL.md`.

## Limites e direitos

Uma auditoria técnica sem erros não certifica fidelidade visual. Resultados dependem das referências, das decisões de modelagem e da revisão de imagens. Validações em uma versão do Blender ou dispositivo não certificam todas as outras configurações.

Esta publicação contém a skill e seus auxiliares, sem cenas, renders, assets de clientes, backups ou o código de integrações de terceiros. Nenhuma licença de código aberto foi adicionada a esta publicação. A disponibilidade pública não substitui uma licença de uso ou redistribuição; consulte o autor para permissões além das fornecidas pela plataforma.
