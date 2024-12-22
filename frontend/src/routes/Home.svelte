<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, is_login, keyword } from "../lib/store" //page 변수인지 객체인지 가져오는 듯
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko');
    
    let question_list = [];
    let size = 10;
    let total = 0;
    let local_keyword = ''
    $: total_page = Math.ceil(total/size);
    //$ : 스벨트에서 앞에 $가 붙으면 반응형 변수다. 
    // api 호출로 인해 값이 변하면 변수도 실시간으로 다시 계산된다는 의미 
      
    function get_question_list() {
        let params = { 
            page: $page,
            size: size, 
            keyword: $keyword
        };
        //page: 현재 페이지 size: 한 페이지 당 몇 개

        //api 방식, url, 빈 params, success_callback, 빈 failuer_callback
        //page랑  size 넘김 
        fastapi('get', '/api/question/list', params, (json) => { 
            question_list = json.question_list;
            total = json.total
            local_keyword = $keyword
        })
        //응답으로 받은 json 데이터를 할당(페이징 이전)
            //question list api의 출력항목이 배열 형태에서 딕셔너리 형태로 바뀜(페이징 이후)
            //question list 데이터가 'question_list'라는 이름으로 전달되어서
            //success_callback 함수에서 json 대신 quesiton_list를 사용해야함
    }
      
   $: $page, $keyword, get_question_list()
   //console.log('get_question_list/keyword : <' + $keyword + '>' + '\npage : ' + $page)
   //page 값이나 keyword 변경될 경우 get_question_list 함수도 다시 호출하라(스벨트 지원)
</script>

<div class = "container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">Register question</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{local_keyword}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = local_keyword, $page = 0}}>Search</button>
            </div>
        </div>
    </div>
    <table class = "table">
        <thead>
            <tr class = "text-center table-dark">
                <th>번호</th>
                <th style = "width:50%">제목</th>
                <th>글쓴이</th>
                <th>작성일시</th>
                <th>답변 개수</th>
            </tr>
        </thead>
        <tbody>
            {#each question_list as question, i} 
            <!--question: 배열의 현재 요소, i: 배열의 현재 인덱스(선택적)-->
            <!--중괄호는 svelte에서 지원하는 템플릿 문법 안에는 js 가능-->
                <tr class = "text-center">
                    <!--교재에서는 total - ($page * size) - i 이렇게 하래..-->
                    <td>{question.id}</td>
                    <td class = "text-start">
                        <a use:link href = "/detail/{question.id}">{question.subject}</a>
                    </td>
                    <td>{ question.user ? question.user.username : "" }</td>
                    <td>{moment(question.create_date).format("YYYY년 MM월 DD일 a hh:mm")}</td>
                    <td>{question.answers.length}</td>
                </tr>
            {/each}
        </tbody>
    </table>
    <!--Strat Paging-->
    <ul class = "pagination justify-content-center">
        <!--First page-->
        <li class = "page-item {$page == 0 && 'disabled'}">
            <button class ="page-link" on:click = "{() => $page = 0}">First Page</button>
        </li>
        <!--Previous page-->
        <li class = "page-item {$page <= 0 && 'disabled'}">
            <!--page가 0 이하면 'disabled'속성을 적용해라-->
            <button class ="page-link" on:click = "{() => $page--}">Previous Page</button>
        </li>
        <!--Page unmber-->
        {#each Array(total_page) as _, loop_page}
            {#if loop_page >= $page - 5 && loop_page <= $page + 5}
                <li class = "page-item {loop_page === $page && 'active'}">
                    <button on:click = "{() => $page = loop_page}" class = "page-link">{loop_page + 1}</button>
                </li>
            {/if}
        {/each}
        <!--Next page--> 
        <li class = "page-item {$page >= total_page - 1 && 'disabled'}">
            <button class = "page-link" on:click = "{() => $page++}">Next Page</button>
        </li>
        <!--Last page-->
        <li class = "page-item {$page == total_page - 1 && 'disabled'}">
            <button class ="page-link" on:click = "{() => $page = total_page - 1}">Last Page</button>
        </li>
    </ul>
    <!--End Paging-->
    <!--<a use:link href = "/question-create" class = "btn btn-primary {$is_login ? '' : 'disabled'}">Register Question</a>-->
</div>
      