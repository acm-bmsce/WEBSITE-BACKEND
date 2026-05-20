package com.example.websitebackend.controller;

import com.example.websitebackend.dto.EventCreateRequest;
import com.example.websitebackend.dto.EventUpdateRequest;
import com.example.websitebackend.model.Event;
import com.example.websitebackend.service.EventService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize; // ✅ IMPORT FOR SECURITY
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/events")
@RequiredArgsConstructor
public class EventController {

    private final EventService eventService;

    // Public route: Anyone visiting the website can see the events
    @GetMapping
    public ResponseEntity<List<Event>> getEvents(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "0") int skip,
            @RequestParam(required = false) Boolean featured
    ) {
        Page<Event> eventPage = eventService.getEvents(skip, limit, featured);
        return ResponseEntity.ok(eventPage.getContent());
    }

    // Locked route: Only Master Admins can create events
    @PreAuthorize("hasRole('MASTER', 'COORDINATOR')")
    @PostMapping
    public ResponseEntity<Event> createEvent(@Valid @RequestBody EventCreateRequest request) {
        Event newEvent = eventService.createEvent(request);
        return new ResponseEntity<>(newEvent, HttpStatus.CREATED);
    }

    // Locked route: Only Master Admins can edit events
    @PreAuthorize("hasRole('MASTER', 'COORDINATOR')")
    @PatchMapping("/{eventId}")
    public ResponseEntity<Event> updateEvent(
            @PathVariable String eventId,
            @RequestBody EventUpdateRequest request
    ) {
        Event updatedEvent = eventService.updateEvent(eventId, request);
        return ResponseEntity.ok(updatedEvent);
    }

    // Locked route: Only Master Admins can delete events
    @PreAuthorize("hasRole('MASTER')")
    @DeleteMapping("/{eventId}")
    public ResponseEntity<Map<String, String>> deleteEvent(@PathVariable String eventId) {
        eventService.deleteEvent(eventId);
        return ResponseEntity.ok(Map.of("message", "Event deleted successfully"));
    }
}