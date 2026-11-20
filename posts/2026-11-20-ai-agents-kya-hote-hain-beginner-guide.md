# AI agents kya hote hain — beginner guide

Language: Hinglish (Roman Hindi mixed with English) | Date: 2026-11-20 | Provider: gemini

Pichle kuch mahino se mere Twitter feed aur GitHub trending page par ek hi term baar-baar dikh raha tha—AI Agents. Dhanbad me apne room me late night code karte waqt maine pehli baar CrewAI aur LangChain ke saath ek chhota setup try kiya. Pehle mujhe laga ye bas ChatGPT ka ek aur marketing term hai, lekin jab maine ek script banayi jo mere Gmail se bills padh kar unko Google Sheets me record kar rahi thi, tab samajh aaya ki ye normal chatbot se alag cheez hai.

Simple terms me kahein toh AI Agent ek aisa software program hai jo kisi goal ko poora karne ke liye khud se decisions leta hai, zaroori tools use karta hai, aur bina kisi continuous human prompt ke step-by-step kaam karta hai.

Normal ChatGPT aur AI Agent me sabse bada farak autonomy ka hai. ChatGPT ek passive system hai—aap sawal poochhte ho, wo text response de deta hai. Agar aap ChatGPT se kaho "Goa trip ki list banao", toh wo text format me itinerary likh dega. Lekin agar aap ek AI Agent ko wahi task doge, toh wo internet browse karega, live flight prices check karega, Python code chala kar budget calculate karega, aur final execution plan ready karke dega. Agent sirf text generate nahi karta, wo actions perform karta hai.

Technical level par dekhein toh ek AI agent ke char main components hote hain. Pehla hai Brain, jo ki ek Large Language Model (jaise GPT-4o ya Claude 3.5 Sonnet) hota hai. LLM ka kaam reasoning karna aur agla step decide karna hota hai.

Doosra component hai Planning. Agent kisi bade task ko chote steps me todta hai. Iske liye ReAct (Reasoning + Acting) pattern use hota hai, jisme agent har step par pehle sochta hai, phir koi action leta hai, aur uska result observe karke agla decision leta hai.

Teesra component hai Tools. Standard LLMs direct internet search nahi kar sakte ya system commands nahi chala sakte. Hum agents ko custom tools dete hain—jaise Web Search API, File System access, ya Python Interpreter. Agent situation ke hisab se decide karta hai ki kab kaun sa tool call karna hai. Chautha component hai Memory, jisme Short-term memory active conversation track karti hai aur Long-term memory (Vector databases jaise ChromaDB ya Pinecone) purane context ko store karke rakhti hai.

Agar aap student ho aur hands-on experiment karna chahte ho, toh Python ke do frameworks sabse popular hain—CrewAI aur LangGraph. CrewAI me aap multi-agent systems bana sakte ho. For example, ek Agent ko researcher bana do jo Google se data nikale, aur doosre Agent ko writer bana do jo us data ko summarize karke report likhe. Dono agents aapas me output pass karke kaam poora karte hain.

Lekin real-world engineering ki baat karein toh agents abhi perfect bilkul nahi hain. Aksar agents infinite loops me phans jaate hain—ek hi API call ko baar-baar repeat karte rehte hain jab tak aapka OpenAI credit limit exhaust na ho jaye. Unka behavior non-deterministic hota hai, yaani ek hi task par har baar alag tareeke se fail ho sakte hain. Production environment me inhe scale karna kaafi expensive aur unpredictable hai.

Filhal status ye hai ki AI agents basic workflows aur automated research ke liye acche hain, lekin ye human developers ko replace nahi kar rahe. Ek student ke naate, mujhe lagta hai ki frameworks use karne se pehle ek basic ReAct loop khud se plain Python me code karke dekhna chahiye. Usse samajh aata hai ki LLM ke peeche ka logic aur tool calling actual me kaise execute hoti hai.
