<script>
    import { push } from 'svelte-spa-router'
    import fastapi from '../lib/api'
    import Error from '../components/Error.svelte'

    let error = {detail: []}
    let subject = ''
    let content = ''

    function post_question(event) {
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            subject: subject,
            content: content,
        }
        
        fastapi('post', url, params, (json) => {
            push("/") //사용자가 질문 등록에 성공하면 홈 페이지로 리디렉션
        }, (json_error) => {
            error = json_error
        })
    }
</script>

<div class = "container">
    <h5 class = "my-3 border-bottom pb-2">Register Question</h5>
    <Error error = {error} />
    <form method = "post" class = "my-3">
        <div class = "mb-3">
            <lable for = "subject">Subject</lable>
            <input type = "text" class = "form-control" bind:value = "{subject}">
        </div>
        <div class = "mb-3">
            <label for = "content">Content</label> 
            <textarea class = "form-control" rows = "10" bind:value = "{content}"></textarea>            
        </div>
        <button class = "btn btn-primary" on:click = "{post_question}">Save</button>
    </form>
</div>