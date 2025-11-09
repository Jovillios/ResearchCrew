from researchcrew.tools.custom_tool import KnowledgeIngestionTool


def test():
    tool = KnowledgeIngestionTool()
    res = tool.run(["https://wdoqeiyrvqpmigzydwys.supabase.co/storage/v1/object/sign/research-documents/ff4b3d50-d3ca-4217-8778-1b86e12c6c7f/1762638892777_pharmaceuticals-16-00253.pdf?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iMTEwOTZhMi1hZDI1LTQ1ZTAtYTQxZi1iOGYzYjQyZmI3MjYiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJyZXNlYXJjaC1kb2N1bWVudHMvZmY0YjNkNTAtZDNjYS00MjE3LTg3NzgtMWI4NmUxMmM2YzdmLzE3NjI2Mzg4OTI3NzdfcGhhcm1hY2V1dGljYWxzLTE2LTAwMjUzLnBkZiIsImlhdCI6MTc2MjYzODk3MCwiZXhwIjoxNzYzMjQzNzcwfQ.SgaHWmK0feqmI406btXHVpILBaDKgDdfXmQZiLc8E_4"])
    print(res)


if __name__ == "__main__":
    test()