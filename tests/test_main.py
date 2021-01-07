from todoist_api_python.main import run


def test_run_prints(capfd):
    run()

    out, err = capfd.readouterr()
    assert out == "hello world\n"
