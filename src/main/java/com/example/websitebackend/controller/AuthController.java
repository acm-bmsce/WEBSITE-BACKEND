package com.example.websitebackend.controller;

import com.example.websitebackend.dto.AuthRequest;
import com.example.websitebackend.model.User;
import com.example.websitebackend.repository.UserRepository;
import com.example.websitebackend.security.CustomUserDetailsService;
import com.example.websitebackend.security.JwtService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final CustomUserDetailsService userDetailsService;
    private final UserRepository userRepository;

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody AuthRequest request) {

        // 1. Authenticate username and password (throws error if invalid)
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );

        // 2. Fetch the user to check their approval status
        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Match your Python logic exactly:
        // if user.role != "master" and not user.is_approved: raise Exception
        if (!user.getRole().equalsIgnoreCase("master") && !user.isApproved()) {
            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("detail", "Account pending approval by Master Admin."));
        }

        // 3. Generate Token
        UserDetails userDetails = userDetailsService.loadUserByUsername(user.getUsername());
        String jwtToken = jwtService.generateToken(userDetails);

        return ResponseEntity.ok(Map.of(
                "access_token", jwtToken,
                "token_type", "bearer"
        ));
    }
}