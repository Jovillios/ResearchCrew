from researchcrew.tools.custom_tool import KnowledgeIngestionTool


def test():
    tool = KnowledgeIngestionTool()
    res = tool.run()
    print(res)


if __name__ == "__main__":
    test()