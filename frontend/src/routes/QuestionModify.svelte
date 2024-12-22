<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    //export는 스벨트 컴포넌트에서 변수를 외부로 노출시키는 역할 
    export let params = {} //외부에서 전달될 변수를 받을 준비하는 코드
    const question_id = params.question_id

    let error = {detail:[]}
    let subject = ''
    let content = ''

    fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
        subject = json.subject
        content = json.content
    })

    function update_question(event) {
        event.preventDefault()
        let url = "/api/question/update"
        let params = {
            question_id: question_id,
            subject: subject,
            content: content,
        }

        fastapi('put', url, params, (json) => {
            push('/detail/' + question_id)
        },
        (json_error) => {
            error = json_error
        })
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Modify Question</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">Subejct</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="content">Content</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_question}">Modify</button>
    </form>
</div>