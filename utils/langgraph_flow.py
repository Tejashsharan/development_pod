# Placeholder for LangGraph implementation if needed.
# from ..agents.business_analyst import analyze_requirements
def orchestrate_agents(requirements):
    # Call agents in order for now
    from agents.bussiness_analyst import analyze_requirements
    # from ..agents.business_analyst import analyze_requirements
    from agents.designer import design_app
    from agents.developer import develop_code
    from agents.tester import test_code

    user_stories = analyze_requirements(requirements)
    design = design_app(user_stories)
    code = develop_code(design)
    test = test_code(code)
    return user_stories, design, code, test
