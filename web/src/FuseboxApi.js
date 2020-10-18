class FuseboxApi {
    constructor() {
        this.baseUrl = 'https://api.fusebox.titomiguelcosta.com';

        this.headers = {
            'user-agent': 'Fusebox Website',
            'content-type': 'application/json',
            'authorization': 'Bearer ' + this.getAccessToken()
        };
    }

    getAccessToken() {
        return sessionStorage.getItem('accessToken');
    }

    setAccessToken(token) {
        return sessionStorage.setItem('accessToken', token);
    }

    getRefreshToken() {
        return sessionStorage.getItem('refreshToken');
    }

    setRefreshToken(token) {
        return sessionStorage.setItem('refreshToken', token);
    }

    async auth(username, password) {
        const response = await fetch(this.baseUrl + '/v1/token/', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'POST',
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const json = await response.json();

        return json;
    };

    async unratedTracks(offset = 0, limit = 10) {
        const response = await fetch(this.baseUrl + '/v1/tracks/unrated?limit=10&offset=0', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'GET',
            redirect: 'follow',
            referrer: 'no-referrer'
        });

        const json = await response.json();

        return json;
    };
}

export default FuseboxApi;