from ai_sidekick import AI_Sidekick

import gradio as gr

async def sidekick_agent_setup():

    sidekick = AI_Sidekick()

    await sidekick.ai_sidekick_setup()

    return sidekick

async def process_user_and_agent_interactions(sidekick, user_input, success_criteria, conversation_history):

    result = await sidekick.execute_graph_superstep(user_input, success_criteria, conversation_history)

    return sidekick, result

async def start_new_session():
    
    new_sidekick_session = AI_Sidekick()

    await new_sidekick_session.ai_sidekick_setup()

    return "","", None, new_sidekick_session

def clear_resources(sidekick):

    print("Clearing up...")
    try:

        if sidekick:

            sidekick.clear_resources()

    except Exception as e:

        print(f"An exception occured during the cleanup process: {e}")

with gr.Blocks(theme=gr.themes.Default(primary_hue='emerald')) as ai_sidekick_user_interface:

  gr.Markdown("AI Sidekick")

  sidekick = gr.State(delete_callback=clear_resources)

  with gr.Row():

    ai_sidekick_bot = gr.Chatbot(label='AI Sidekick', height= 300, type= 'messages')

    with gr.Group():

      with gr.Row():

        input = gr.Textbox(show_label= False, placeholder = 'Input your request here')

      with gr.Row():

        success_criteria = gr.Textbox(show_label = False, placeholder= 'Specify your expected success criteria') 

      with gr.Row():

        start_new_session_button = gr.Button('Start new session', variant = 'stop')

        begin_task_button = gr.Button('Begin task', variant = 'primary')

      ai_sidekick_user_interface.load(sidekick_agent_setup, [], [sidekick])
      
      input.submit(process_user_and_agent_interactions,[sidekick, input, success_criteria,ai_sidekick_bot], [ai_sidekick_bot, sidekick])

      success_criteria.submit(process_user_and_agent_interactions, [sidekick, input, success_criteria, ai_sidekick_bot], [ai_sidekick_bot, sidekick])

      begin_task_button.click(process_user_and_agent_interactions, [sidekick, input, success_criteria, ai_sidekick_bot], [ai_sidekick_bot, sidekick])

      start_new_session_button.click(start_new_session, [], [input, success_criteria, ai_sidekick_bot, sidekick])


      