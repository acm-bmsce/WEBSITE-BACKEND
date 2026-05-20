package com.example.websitebackend.controller;

import com.example.websitebackend.dto.InsightCreateRequest;
import com.example.websitebackend.dto.InsightUpdateRequest;
import com.example.websitebackend.model.Insight;
import com.example.websitebackend.service.InsightService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/insights")
@RequiredArgsConstructor
public class InsightController {

    private final InsightService insightService;

    @GetMapping
    public ResponseEntity<List<Insight>> getInsights(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "0") int skip
    ) {
        Page<Insight> insights = insightService.getInsights(skip, limit);
        return ResponseEntity.ok(insights.getContent());
    }

    @PreAuthorize("hasRole('MASTER', 'COORDINATOR')")
    @PostMapping
    public ResponseEntity<Insight> createInsight(@Valid @RequestBody InsightCreateRequest request) {
        Insight newInsight = insightService.createInsight(request);
        return new ResponseEntity<>(newInsight, HttpStatus.CREATED);
    }

    @PreAuthorize("hasRole('MASTER', 'COORDINATOR')")
    @PatchMapping("/{id}")
    public ResponseEntity<Insight> updateInsight(
            @PathVariable String id,
            @RequestBody InsightUpdateRequest request
    ) {
        Insight updatedInsight = insightService.updateInsight(id, request);
        return ResponseEntity.ok(updatedInsight);
    }

    @PreAuthorize("hasRole('MASTER')")
    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deleteInsight(@PathVariable String id) {
        insightService.deleteInsight(id);
        return ResponseEntity.ok(Map.of("message", "Deleted successfully"));
    }
}