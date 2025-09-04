議題: ${debate.topic}

【参加エージェント一覧】
% for agent in agents:
- ${agent.name}: ${agent.persona_prompt}
% endfor

【これまでの会話履歴】
% for msg in messages:
[${msg.turn}] ${msg.agent.name}: ${msg.content}
% endfor

【次の発言者】
${next_agent.name}（ペルソナ: ${next_agent.persona_prompt}）

あなたはAIディベートの進行役です。次の発言者が議論をどう進めるべきか、ModeratorResponseスキーマに従い、statement（発言内容）、reasoning（その根拠）、conclusion_reason（議論が終了すべき場合のみ理由）をJSONで返してください。
