const calcMD5 = require('./lib/md5');
const request = require('request-promise');

const baseURL = 'http://172.16.254.19:8080/Self/nav_login'
const loginURL = 'http://172.16.254.19:8080/Self/LoginAction.action'
const loggedURL = 'http://172.16.254.19:8080/Self/nav_offLine'
const params = {
    account: 'E21714049',
    password: calcMD5('131452'),
    code: '',
    checkCode: '',
    Submit: 'Login'
}
const session = request.defaults({ jar: true });

async function getCurrentIP() {
    const res = await session.get(baseURL);
    
    params.checkCode = res.match(/checkcode="(\d{4})"/)[1];
    const result = await session.post(loginURL, { form: params });

    console.log(result);
}

getCurrentIP();
