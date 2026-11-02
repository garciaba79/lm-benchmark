# Phi 4
Model: microsoft/phi-4
Test: Category 2
Created: 11/01/2026, 11:46:03 PM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Your task is to assign each piece of information (or “memory”) to one or more of the following categories. Feel free to use multiple categories per item when appropriate.

- Personal: family, friends, home, hobbies, lifestyle
- Relationships: social network, significant others, colleagues
- Preferences: likes, dislikes, habits, favorite media
- Health: physical fitness, mental health, diet, sleep
- Travel: trips, commutes, favorite places, itineraries
- Work: job roles, companies, projects, promotions
- Education: courses, degrees, certifications, skills development
- Projects: to-dos, milestones, deadlines, status updates
- AI, ML & Technology: infrastructure, algorithms, tools, research
- Technical Support: bug reports, error logs, fixes
- Finance: income, expenses, investments, billing
- Shopping: purchases, wishlists, returns, deliveries
- Legal: contracts, policies, regulations, privacy
- Entertainment: movies, music, games, books, events
- Messages: emails, SMS, alerts, reminders
- Customer Support: tickets, inquiries, resolutions
- Product Feedback: ratings, bug reports, feature requests
- News: articles, headlines, trending topics
- Organization: meetings, appointments, calendars
- Goals: ambitions, KPIs, long-term objectives

Guidelines:
- Return ONLY a comma-delimited list of categories (e.g., Personal, Preferences, Work).
- Do not include any explanations, numbering, or additional text.
- If you cannot categorize the memory, return an empty response.
- Don't limit yourself to the categories listed above only. Feel free to create new categories based on the memory. Make sure each category is a single concise phrase.

Memory to categorize:
"Yesterday I experimented with fine-tuning a Llama 3.1 model on my custom dataset of medical texts using Hugging Face Transformers and PEFT for efficiency. Ran into VRAM overflow on my GPU, but switched to 4-bit quantization and it worked. Thrilled with the initial accuracy boost—aiming to deploy it for a health app prototype by next month."

Categories (comma-delimited list only):

> #### 🤖 Assistant

AI, ML & Technology, Projects, Health, Technical Support, Work

78 t/s, 15 tokens, 0s, 3%
