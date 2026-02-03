# Spring Security 7 Migration Reference

Complete guide for migrating from Spring Security 6.x to 7.x in Spring Boot 4.

---

## Overview

Spring Security 7.0 is a major release with:
- Lambda-only DSL (`.and()` method removed)
- `authorizeRequests` removed (use `authorizeHttpRequests`)
- New path matching with `PathPatternRequestMatcher`
- Jackson 3 integration
- Authorization Server merged into main project

---

## Preparation

### Upgrade Path

1. First upgrade to Spring Security 6.5 (with Spring Boot 3.5)
2. Fix all deprecation warnings
3. Then upgrade to Spring Security 7.0 (with Spring Boot 4.0)

Spring Security 6.5 provides preparation strategies for breaking changes.

---

## DSL Changes

### Remove `.and()` Chaining

```java
// Spring Security 6.x - and() chaining
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .and()
        .formLogin()
        .and()
        .httpBasic();
    return http.build();
}

// Spring Security 7.x - Lambda only
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .httpBasic(Customizer.withDefaults());
    return http.build();
}
```

### Lambda Configuration Examples

```java
// Form Login with custom configuration
http.formLogin(form -> form
    .loginPage("/login")
    .loginProcessingUrl("/authenticate")
    .defaultSuccessUrl("/home")
    .failureUrl("/login?error")
    .permitAll()
);

// HTTP Basic with custom realm
http.httpBasic(basic -> basic
    .realmName("My App Realm")
);

// CSRF with custom handling
http.csrf(csrf -> csrf
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
    .ignoringRequestMatchers("/api/webhooks/**")
);

// CORS configuration
http.cors(cors -> cors
    .configurationSource(corsConfigurationSource())
);

// Session management
http.sessionManagement(session -> session
    .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
);

// Exception handling
http.exceptionHandling(exceptions -> exceptions
    .authenticationEntryPoint(customEntryPoint())
    .accessDeniedHandler(customAccessDeniedHandler())
);
```

### Disable Feature with Lambda

```java
// Spring Security 6.x
http.csrf().disable();

// Spring Security 7.x
http.csrf(csrf -> csrf.disable());
// or
http.csrf(AbstractHttpConfigurer::disable);
```

---

## Authorization Changes

### Replace `authorizeRequests` with `authorizeHttpRequests`

```java
// Spring Security 6.x (deprecated)
http.authorizeRequests()
    .antMatchers("/public/**").permitAll()
    .antMatchers("/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated();

// Spring Security 7.x
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/public/**").permitAll()
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated()
);
```

### Request Matchers

```java
// Spring Security 6.x - AntPathRequestMatcher
new AntPathRequestMatcher("/api/**")
new AntPathRequestMatcher("/api/**", "GET")

// Spring Security 7.x - PathPatternRequestMatcher (preferred)
PathPatternRequestMatcher.pathPattern("/api/**")
PathPatternRequestMatcher.pathPattern(HttpMethod.GET, "/api/**")

// Or use requestMatchers() in DSL
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/**").hasRole("USER")
    .requestMatchers(HttpMethod.POST, "/api/write/**").hasRole("WRITER")
);
```

### Method Security

```java
// Enable method security
@Configuration
@EnableMethodSecurity
public class SecurityConfig {
}

// Use in code
@PreAuthorize("hasRole('ADMIN')")
public void adminOperation() {}

@PostAuthorize("returnObject.owner == authentication.name")
public Resource getResource(Long id) {}

// Compile with --parameters if using method parameter names
@PreAuthorize("#id == authentication.principal.id")
public User getUser(Long id) {}
```

### AuthorizationAdvisor Changes

```java
// Spring Security 6.x - Manual advisor configuration
AuthorizationAdvisorProxyFactory factory = new AuthorizationAdvisorProxyFactory();
factory.setAdvisors(customAdvisor);

// Spring Security 7.x - Publish as bean (auto-discovered)
@Bean
public AuthorizationAdvisor customAdvisor() {
    return new MyCustomAuthorizationAdvisor();
}
```

---

## Jackson 3 Integration

### Security Jackson Modules

```java
// Spring Security 6.x with Jackson 2
ObjectMapper mapper = new ObjectMapper();
ClassLoader classLoader = getClass().getClassLoader();
mapper.registerModules(SecurityJackson2Modules.getModules(classLoader));

// Spring Security 7.x with Jackson 3
JsonMapper.Builder builder = JsonMapper.builder();
SecurityJacksonModules.configure(builder);
JsonMapper mapper = builder.build();
```

### OAuth2 Authorization Server Jackson

```java
// Spring Security 7.x
// Jackson 3 is default. To use Jackson 2 temporarily:

// pom.xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-authorization-server</artifactId>
    <exclusions>
        <exclusion>
            <groupId>tools.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
```

---

## OAuth 2.0 Changes

### Starter Renames

```xml
<!-- Old (3.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>

<!-- New (4.x) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-client</artifactId>
</dependency>
```

### Authorization Server

Spring Authorization Server is now part of Spring Security 7.0:

```xml
<!-- Maven coordinate unchanged, but version managed by spring-security.version -->
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-authorization-server</artifactId>
</dependency>
```

To override version:
```xml
<properties>
    <!-- OLD: spring-authorization-server.version - no longer works -->
    <!-- NEW: Use spring-security.version -->
    <spring-security.version>7.0.0</spring-security.version>
</properties>
```

### Resource Server Configuration

```java
@Bean
public SecurityFilterChain resourceServerFilterChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/public/**").permitAll()
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2
            .jwt(jwt -> jwt
                .jwtAuthenticationConverter(jwtAuthenticationConverter())
            )
        );
    return http.build();
}
```

---

## Authentication Changes

### Authentication.Builder

New fluent API for mutating Authentication:

```java
// Spring Security 7.x
Authentication modified = Authentication.builder(existingAuth)
    .authorities(newAuthorities)
    .details(newDetails)
    .build();
```

### Custom Authentication Providers

```java
@Bean
public AuthenticationManager authenticationManager(
        AuthenticationConfiguration config) throws Exception {
    return config.getAuthenticationManager();
}

@Bean
public AuthenticationProvider customAuthProvider() {
    return new CustomAuthenticationProvider();
}
```

---

## Access API Module

Legacy Access Decision API moved to separate module:

```xml
<!-- Only if using legacy AccessDecisionManager/AccessDecisionVoter -->
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-access</artifactId>
</dependency>
```

**Recommendation:** Migrate to new `AuthorizationManager` API instead.

```java
// Old - AccessDecisionManager
// New - AuthorizationManager
http.authorizeHttpRequests(auth -> auth
    .anyRequest().access(customAuthorizationManager())
);

@Bean
public AuthorizationManager<RequestAuthorizationContext> customAuthorizationManager() {
    return (authentication, context) -> {
        // Custom authorization logic
        return new AuthorizationDecision(true);
    };
}
```

---

## Testing Changes

### Test Starter Required

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

### Security Test Annotations

```java
// @WithMockUser - unchanged usage
@Test
@WithMockUser(username = "admin", roles = {"ADMIN"})
void adminEndpoint() {}

// @WithUserDetails - unchanged usage
@Test
@WithUserDetails("admin@example.com")
void withRealUser() {}

// MockMvc security setup
@AutoConfigureMockMvc
@SpringBootTest
class SecurityTest {
    @Autowired
    private MockMvc mockMvc;

    @Test
    void testSecuredEndpoint() throws Exception {
        mockMvc.perform(get("/api/data")
                .with(SecurityMockMvcRequestPostProcessors.jwt()))
            .andExpect(status().isOk());
    }
}
```

---

## Common Configuration Patterns

### Basic Web Security

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/", "/home", "/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .permitAll()
            )
            .logout(logout -> logout
                .logoutSuccessUrl("/")
                .permitAll()
            );
        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### REST API Security

```java
@Configuration
@EnableWebSecurity
public class ApiSecurityConfig {

    @Bean
    public SecurityFilterChain apiFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.GET, "/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(Customizer.withDefaults())
            );
        return http.build();
    }
}
```

### Multiple Security Filter Chains

```java
@Configuration
@EnableWebSecurity
public class MultiSecurityConfig {

    @Bean
    @Order(1)
    public SecurityFilterChain apiFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
        return http.build();
    }

    @Bean
    @Order(2)
    public SecurityFilterChain webFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/login", "/register").permitAll()
                .anyRequest().authenticated()
            )
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

---

## Migration Checklist

- [ ] Remove all `.and()` calls, use lambda configuration
- [ ] Replace `authorizeRequests()` with `authorizeHttpRequests()`
- [ ] Replace `antMatchers()` with `requestMatchers()`
- [ ] Update to `PathPatternRequestMatcher` where applicable
- [ ] Update Jackson configuration to Jackson 3
- [ ] Rename OAuth2 starters
- [ ] Add `spring-boot-starter-security-test` for test annotations
- [ ] Update `spring-security.version` property (not `spring-authorization-server.version`)
- [ ] Compile with `--parameters` if using method parameter names in SpEL
- [ ] Test all secured endpoints
- [ ] Test OAuth2 flows if applicable
