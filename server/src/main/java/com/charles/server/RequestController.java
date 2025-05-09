package com.charles.server;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RequestController {
    @RequestMapping("/request")
    public String request(HttpServletRequest request) {
        // 1. 获取请求方式
        System.out.println("请求方式: "+request.getMethod());

        // 2. 获取请求路径
        System.out.println("URL: "+request.getRequestURL());
        System.out.println("URI: "+request.getRequestURI());

        // 3. 获取请求协议
        System.out.println("协议: "+request.getProtocol());

        // 4. 获取请求参数
        System.out.println("请求参数name: "+request.getParameter("name"));
        System.out.println("请求参数age: "+request.getParameter("age"));

        // 5. 获取请求头
        System.out.println("请求头Accept: "+request.getHeader("Accept"));

        return "{\"sever\":\"IIA\"}";

        // http://localhost:8081/request?name=charles&age=18

        // 请求方式: GET
        // URL: http://localhost:8081/request
        // URI: /request
        // 协议: HTTP/1.1
        // 请求参数name: charles
        // 请求参数age: 18
        // 请求头Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    }
}
