<script>
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte";
    import { link, push } from 'svelte-spa-router';
    import { is_login, username } from "../lib/store";
    import moment from 'moment/min/moment-with-locales';
    moment.locale('ko');

    export let params = {}
    let question_id = params.question_id
    let question = {answers: [], recommend: []} //question 변수의 초깃값 설정?
    let content = ""
    let error = {detail:[]} //detail 항목의 값이 비워진 형태 
    //console.log('question_id:' + question_id)

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {question = json})
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        let params = { content: content } //params는 api에 전달할 데이터
        fastapi('post', url, params, (json) => {
            content = ''; error = {detail:[]}; get_question();
            //success 하면 이전의 에러 변수 초기화
        }, (err_json) => {
            error = err_json 
            //err_json이 {detail: ...} 형태로 전달됨, error 변수에 오류 내용 저장
            //error 변수는 Error 컴포넌트랑 연결되어 있어서 오류가 표시됨 (?)
        })
    }

    function delete_question(delete_question_id) {
        if(window.confirm('Are you sure to delete question?')) {
            let url = "/api/question/delete"
            let params = {
                question_id: delete_question_id
            }
            fastapi('delete', url, params, (json) => {
                push('/')
            }, (err_json) => {
                error = err_json
            })
        }
    }

    function delete_answer(delete_answer_id) {
        if(window.confirm("Are you sure to delete answer?")) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: delete_answer_id
            }
            fastapi('delete', url, params, (json) => {
                    get_question()
                }, (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function recommend_question(recommend_question_id) {
        if(window.confirm('Are you sure to recommend?')) {
            let url = "/api/question/recommend"
            let params = {
                question_id: recommend_question_id
            }
            fastapi('post', url, params, (json) => {
                    get_question()
                }, (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function recommend_answer(recommend_answer_id) {
        if(window.confirm('Are you sure to recommend?')) {
            let url = "/api/answer/recommend"
            let params = {
                answer_id: recommend_answer_id
            }
            fastapi('post', url, params, (json) => {
                    get_question()
                }, (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<div class = "container my-3">
    <!--question-->
    <h2 class = "border-bottom py-2">{question.subject}</h2>
    <div class = "card my-3">
        <div class = "card-body">
            <div class = "card-text" style = "white-space: pre-line;">
                {question.content}
            </div>
            <div class = "d-flex justify-content-end">
                {#if question.modify_date}
                    <div class = "badge bg-light text-dark p-2 text-start max-3">
                        <div class = "mb-2">Modified at</div>
                        <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 a hh:mm")}</div>
                    </div>
                {/if}
                <div class = "badge bg-light text-dark p-2 text-start">
                    <div class = "mb-2">Writer : { question.user ? question.user.username : "" }</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 a hh:mm")}</div>
                </div>
            </div>
            <!--Modify question button-->
            <div class = "my-3">
                <button class="btn btn-sm btn-outline-secondary" on:click="{recommend_question(question.id)}">Recommend
                    <span class="badge rounded-pill bg-success">{ question.recommend.length }</span>
                </button>
                {#if question.user && $username === question.user.username}
                    <a use:link href = "/question-modify/{question.id}" class = "btn btn-sm btn-outline-secondary">Modify</a>
                    <button class = "btn btn-sm btn-outline-secondary" on:click = {() => delete_question(question.id)}>delete</button>
                {/if}
            </div>
        </div>
    </div>

    <!--answer list-->
    <h5 class = "border-bottom my-3 py-2">
        {question.answers.length} of answers
    </h5>
    {#each question.answers as answer}
        <div class = "card my-3">
            <div class = "card-body">
                <div class = "card-text" style = "white-space: pre-line;">
                    {answer.content}
                </div>
                <div class = "d-flex justify-content-end">
                    {#if answer.modify_date }
                        <div class="badge bg-light text-dark p-2 text-start mx-3">
                            <div class="mb-2">modified at</div>
                            <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                        </div>
                    {/if}
                    <div class = "badge bg-light text-dark p-2 text-start">
                        <div class = "mb-2">Writer : { answer.user ? answer.user.username : "" }</div>
                        <div>{moment(question.create_date).format("YYYY년 MM월 DD일 a hh:mm")}</div>
                    </div>
                </div>
                <div class = "my-3">
                    <button class="btn btn-sm btn-outline-secondary" on:click="{recommend_answer(answer.id)}">recommend 
                        <span class="badge rounded-pill bg-success">{ answer.recommend.length }</span>
                    </button>
                    {#if answer.user && $username === answer.user.username}
                        <a use:link href = "/answer-modify/{answer.id}" class = "btn btn-sm btn-outline-secondary">Modify</a>
                        <button class = "btn btn-sm btn-outline-secondary" on:click = {() => delete_answer(answer.id)}>Delete</button>
                    {/if}
                </div>
            </div>
        </div>
    {/each}
    <!--submit answer-->
    <Error error = {error} /> <!--오류 발생 확인할 수 있게-->
    <form method = "post" class = "my-3">
        <div class = "mb-3">
            <textarea rows = "10" bind:value = {content} 
                disabled = {$is_login ? "" : "disabled"}
                class = "form-control"></textarea>
        </div>
        <input type = "submit" value = "Register Answer" class = "btn btn-primary {$is_login ? '' :'disabled'}" on:click = "{post_answer}"/>
    </form>
    
    <button class = "btn btn-secondary" on:click = "{() => {push('/')}}">List</button>

</div>
