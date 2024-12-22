<script>
    import Router from 'svelte-spa-router'
    import Home from "./routes/Home.svelte"
    import Detail from "./routes/Detail.svelte"
    import QuestionCreate from "./routes/QuestionCreate.svelte"
    import Navigation from "./components/Navigation.svelte"
    import UserCreate from "./routes/UserCreate.svelte"
    import UserLogin from "./routes/UserLogin.svelte"
    import QuestionModify from "./routes/QuestionModify.svelte"
    import AnswerModify from "./routes/AnswerModify.svelte"
    //이 코드로 UserLogin.svelte 컴포넌트 가져와서 UserLogin이라는 변수에 저장 

    // UserLogin은 컴포넌트 (컴포넌트란 .svelte 파일이 하나의 컴포넌트; 
    // HTML, CSS, JS 코드가 섞여서 특정 UI의 한 부분을 만드는 독립적인 단위)
    
    const routes = {
        '/': Home,
        '/detail/:question_id': Detail,
        '/question-create': QuestionCreate,
        '/user-create': UserCreate,
        '/user-login': UserLogin, //위에서 가져온 컴포넌트 참조
        '/question-modify/:question_id': QuestionModify,
        '/answer-modify/:answer_id': AnswerModify,
    }
    //결과적으로 /user-login 경로가 요청되면 UserLogin.svlete 컴포넌트가 렌더링된다.
    
</script>

<Navigation />
<Router {routes}/>